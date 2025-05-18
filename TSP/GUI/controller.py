import numpy as np
from PyQt6.QtCore import QTimer
from model import Graph, Colony
from view import ACOApp

class ACOController:
    def __init__(self):
        self.view = ACOApp()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_iteration)

        self.iter_count = 0
        self.running = False

        # Initialize parameters and colony
        self.reset()

        # Connect buttons and parameter changes
        self.view.start_btn.clicked.connect(self.start)
        self.view.stop_btn.clicked.connect(self.stop)
        self.view.reset_btn.clicked.connect(self.reset)

        self.view.spin_cities.valueChanged.connect(self.params_changed)
        self.view.spin_ants.valueChanged.connect(self.params_changed)
        self.view.spin_iters.valueChanged.connect(self.params_changed)
        self.view.spin_alpha.valueChanged.connect(self.params_changed)
        self.view.spin_beta.valueChanged.connect(self.params_changed)
        self.view.spin_rho.valueChanged.connect(self.params_changed)
        self.view.spin_Q.valueChanged.connect(self.params_changed)

    def params_changed(self):
        if self.running:
            self.stop()
        self.reset()

    def reset(self):
        self.iter_count = 0
        self.best_costs = []
        self.avg_costs = []
        self.best_paths = []

        self.num_cities = self.view.spin_cities.value()
        self.num_ants = self.view.spin_ants.value()
        self.iterations = self.view.spin_iters.value()
        self.alpha = self.view.spin_alpha.value()
        self.beta = self.view.spin_beta.value()
        self.rho = self.view.spin_rho.value()
        self.Q = self.view.spin_Q.value()

        self.dist_matrix = Graph.generate_distances(self.num_cities)
        self.graph = Graph(self.num_cities, self.dist_matrix)
        self.colony = Colony(self.num_cities, self.dist_matrix, self.num_ants, self.alpha, self.beta, self.rho, self.Q)

        self.city_coords = np.random.uniform(5, 100, (self.num_cities, 2))

        # Clear plots
        self.view.ax_map.clear()
        self.view.ax_map.set_title("Cities and Best Path")
        self.view.ax_map.set_xlim(0, 110)
        self.view.ax_map.set_ylim(0, 110)
        self.view.ax_map.scatter(self.city_coords[:, 0], self.city_coords[:, 1], c='black', s=50, label='Cities')
        self.view.best_path_line, = self.view.ax_map.plot([], [], 'r-', linewidth=2, label='Best Path')
        self.view.ant_dots, = self.view.ax_map.plot([], [], 'go', markersize=8, label='Ants')
        self.view.ax_map.legend()

        self.view.ax_cost.clear()
        self.view.ax_cost.set_title("Best Cost and Average Cost Evolution")
        self.view.ax_cost.set_xlabel("Iteration")
        self.view.ax_cost.set_ylabel("Cost")
        self.view.ax_cost.grid(True)

        self.cost_line, = self.view.ax_cost.plot([], [], 'r-', label='Best Cost')

        self.avg_cost_line, = self.view.ax_cost.plot([], [], 'b--', label='Average Cost')

        self.view.ax_cost.legend()
        self.view.progress_bar.setValue(0)
        self.view.label.setText("Best Cost: N/A")

        self.view.canvas.draw()

    def start(self):
        if self.running:
            return
        self.running = True
        self.timer.start(100)  # update every 100ms

    def stop(self):
        if not self.running:
            return
        self.running = False
        self.timer.stop()

    def update_iteration(self):
        if self.iter_count >= self.iterations:
            self.stop()
            return

        best_cost, best_path, ants, avg_cost = self.colony.run_iteration()
        self.best_costs.append(best_cost)
        self.avg_costs.append(avg_cost)
        self.best_paths.append(best_path)

        # Update GUI
        self.view.progress_bar.setValue(int((self.iter_count + 1) / self.iterations * 100))
        self.view.label.setText(f"Best Cost: {best_cost:.2f}")

        # Plot best path on map
        coords = self.city_coords
        path = best_path + [best_path[0]]
        x = coords[path, 0]
        y = coords[path, 1]
        self.view.best_path_line.set_data(x, y)

        # Plot ants current positions (last city in their path)
        ant_positions = [coords[ant.path[-1]] if ant.path else (0, 0) for ant in ants]
        ax = self.view.ax_map
        self.view.ant_dots.set_data([pos[0] for pos in ant_positions], [pos[1] for pos in ant_positions])

        # Update cost plot
        self.cost_line.set_data(range(len(self.best_costs)), self.best_costs)
        self.avg_cost_line.set_data(range(len(self.avg_costs)), self.avg_costs)

        self.view.ax_cost.relim()
        self.view.ax_cost.autoscale_view()

        self.view.canvas.draw()
        self.iter_count += 1

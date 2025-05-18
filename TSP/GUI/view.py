from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QHBoxLayout, QSpinBox, QFormLayout, QGroupBox,
    QDoubleSpinBox, QProgressBar
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class ACOApp(QWidget):
    def __init__(self):
        super().__init__()
        self.best_costs = []
        self.avg_costs = []
        self.setWindowTitle("Ant Colony Optimization with Dynamic GUI and Plots")
        self.setWindowIcon(QIcon("icon.png"))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Controls group
        controls_group = QGroupBox("Settings")
        controls_layout = QFormLayout()

        self.spin_cities = QSpinBox()
        self.spin_cities.setRange(5, 50)
        controls_layout.addRow("Number of Cities:", self.spin_cities)

        self.spin_ants = QSpinBox()
        self.spin_ants.setRange(1, 100)
        controls_layout.addRow("Number of Ants:", self.spin_ants)

        self.spin_iters = QSpinBox()
        self.spin_iters.setRange(10, 500)
        controls_layout.addRow("Iterations:", self.spin_iters)

        self.spin_alpha = QDoubleSpinBox()
        self.spin_alpha.setRange(0.1, 5.0)
        self.spin_alpha.setSingleStep(0.1)
        controls_layout.addRow("Alpha (pheromone importance):", self.spin_alpha)

        self.spin_beta = QDoubleSpinBox()
        self.spin_beta.setRange(0.1, 10.0)
        self.spin_beta.setSingleStep(0.1)
        controls_layout.addRow("Beta (distance importance):", self.spin_beta)

        self.spin_rho = QDoubleSpinBox()
        self.spin_rho.setRange(0.01, 1.0)
        self.spin_rho.setSingleStep(0.01)
        controls_layout.addRow("Evaporation rate (rho):", self.spin_rho)

        self.spin_Q = QDoubleSpinBox()
        self.spin_Q.setRange(10, 500)
        self.spin_Q.setSingleStep(10)
        controls_layout.addRow("Q (pheromone deposit):", self.spin_Q)

        controls_group.setLayout(controls_layout)
        self.layout.addWidget(controls_group)

        # Buttons
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Start")
        self.stop_btn = QPushButton("Stop")
        self.reset_btn = QPushButton("Reset")
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.reset_btn)
        self.layout.addLayout(btn_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.layout.addWidget(self.progress_bar)

        self.label = QLabel("Best Cost: N/A")
        self.layout.addWidget(self.label)

        # Matplotlib figures and canvases
        self.fig = Figure(figsize=(12, 6))
        self.canvas = FigureCanvas(self.fig)
        self.layout.addWidget(self.canvas)

        # Subplots
        self.ax_map = self.fig.add_subplot(121)
        self.ax_cost = self.fig.add_subplot(122)

        self.ax_map.set_title("Cities and Best Path")
        self.ax_map.set_xlim(0, 110)
        self.ax_map.set_ylim(0, 110)

        self.ax_cost.set_title("Best Cost Evolution")
        self.ax_cost.set_xlabel("Iteration")
        self.ax_cost.set_ylabel("Cost")
        self.ax_cost.grid(True)

        self.city_scatter = self.ax_map.scatter([], [], c='black', s=50, label='Cities')
        self.best_path_line, = self.ax_map.plot([], [], 'r-', linewidth=2, label='Best Path')
        self.ant_dots, = self.ax_map.plot([], [], 'go', markersize=8, label='Ants')

        self.ax_map.legend()

import numpy as np
import random

class Graph:
    def __init__(self, num_cities, dist_matrix=None, low=3, high=50):
        self.num_cities = num_cities
        if dist_matrix is not None:
            self.dist_matrix = dist_matrix
        else:
            self.dist_matrix = self.generate_distances(num_cities, low, high)

    @staticmethod
    def generate_distances(num_cities, low=3, high=50):
        dist = np.zeros((num_cities, num_cities), dtype=int)
        for i in range(num_cities):
            for j in range(i + 1, num_cities):
                distance = random.randint(low, high)
                dist[i, j] = dist[j, i] = distance
        return dist

    @staticmethod
    def path_cost(path, dist_matrix):
        cost = 0
        for i in range(len(path) - 1):
            cost += dist_matrix[path[i], path[i + 1]]
        cost += dist_matrix[path[-1], path[0]]
        return cost

class Ant:
    def __init__(self, num_cities, dist_matrix, pheromone, alpha=1, beta=5):
        self.num_cities = num_cities
        self.dist_matrix = dist_matrix
        self.pheromone = pheromone
        self.alpha = alpha
        self.beta = beta
        self.path = []
        self.visited = set()

    def select_next_city(self):
        current = self.path[-1]
        unvisited = [c for c in range(self.num_cities) if c not in self.visited]
        if not unvisited:
            return None

        probabilities = []
        denom = 0
        for city in unvisited:
            tau = self.pheromone[current][city] ** self.alpha
            eta = (1 / self.dist_matrix[current][city]) ** self.beta
            denom += tau * eta

        for city in unvisited:
            tau = self.pheromone[current][city] ** self.alpha
            eta = (1 / self.dist_matrix[current][city]) ** self.beta
            prob = (tau * eta) / denom if denom > 0 else 0
            probabilities.append(prob)

        r = random.random()
        cum_sum = 0
        for city, prob in zip(unvisited, probabilities):
            cum_sum += prob
            if r <= cum_sum:
                return city
        return unvisited[-1]

    def build_path(self):
        start = random.randint(0, self.num_cities - 1)
        self.path = [start]
        self.visited = {start}
        while len(self.visited) < self.num_cities:
            next_city = self.select_next_city()
            if next_city is None:
                break
            self.path.append(next_city)
            self.visited.add(next_city)

class Colony:
    def __init__(self, num_cities, dist_matrix, num_ants=10, alpha=1, beta=5, rho=0.1, Q=100):
        self.num_cities = num_cities
        self.dist_matrix = dist_matrix
        self.num_ants = num_ants
        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.Q = Q
        self.pheromone = np.ones((num_cities, num_cities))
        self.best_path = None
        self.best_cost = float('inf')

    def run_iteration(self):
        ants = [Ant(self.num_cities, self.dist_matrix, self.pheromone, self.alpha, self.beta) for _ in range(self.num_ants)]
        for ant in ants:
            ant.build_path()

        delta = np.zeros_like(self.pheromone)
        costs = []
        for ant in ants:
            L = Graph.path_cost(ant.path, self.dist_matrix)
            costs.append(L)
            if L < self.best_cost:
                self.best_cost = L
                self.best_path = ant.path.copy()
            for i in range(len(ant.path) - 1):
                x, y = ant.path[i], ant.path[i + 1]
                delta[x, y] += self.Q / L
                delta[y, x] += self.Q / L
            x, y = ant.path[-1], ant.path[0]
            delta[x, y] += self.Q / L
            delta[y, x] += self.Q / L

        self.pheromone = self.pheromone * (1 - self.rho) + delta
        avg_cost = sum(costs) / len(costs)
        return self.best_cost, self.best_path, ants, avg_cost

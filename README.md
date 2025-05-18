# Ant Colony Optimization for TSP

This project implements the Ant Colony Optimization (ACO) algorithm to solve the Traveling Salesman Problem (TSP). The implementation includes both a GUI application and Jupyter notebooks for algorithm analysis and visualization.

## Project Structure

```
TSP/
├── GUI/
│   ├── view.py         # PyQt6 interface definition
│   ├── model.py        # ACO algorithm core implementation
│   ├── controller.py   # Connects the view and model
│   └── main.py         # Application entry point
├── Notebooks/
│   ├── ACO_TSP_one_path.ipynb   # Analysis of ACO on different TSP instances
│   └── ACO_TSP_partial_path.ipynb  # Modified version with full path building
├── requirements.txt    # Dependencies for the project
└── README.md           # Project documentation
```

## About Ant Colony Optimization

Ant Colony Optimization (ACO) is a metaheuristic inspired by the foraging behavior of ants. For solving the Traveling Salesman Problem:

1. **Virtual ants** traverse the graph, building paths between cities
2. **Pheromone trails** are laid on edges based on path quality
3. **Probability-based movement** directs ants toward promising paths
4. **Pheromone evaporation** prevents premature convergence

The algorithm balances:
- **Exploration**: Finding new potential solutions
- **Exploitation**: Refining existing good solutions

## Features

### GUI Application
- Interactive parameter tuning
- Real-time visualization of:
  - Cities and best path found
  - Ant positions during search
  - Best cost evolution over iterations
  - Average cost across all ants
- Progress tracking and controls for starting/stopping optimization

### Parameter Controls
- Number of cities
- Number of ants
- Iterations
- Alpha (pheromone importance)
- Beta (distance importance)
- Rho (evaporation rate)
- Q (pheromone deposit amount)

### Notebooks
The notebooks provide analysis of ACO performance with different parameters:
- Effect of ant population size (1, 5, 10, 20 ants)
- Performance comparison between 10 and 20 city problems
- Visualization of pheromone matrix evolution
- Comparison of best vs. average costs

## Algorithm Implementation

Two versions of the algorithm are implemented:
1. **Partial Path Building**: Ants first build partial paths, then similar paths are combined
2. **Full Path Building**: Each ant builds a complete tour independently

## Installation & Usage

### Requirements
- Python 3.6+
- PyQt6
- NumPy
- Matplotlib
- Seaborn (for notebooks)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/Manounnaa/Optimization-Algorithms-Tetris-TSP.git
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the GUI Application
```bash
cd TSP/GUI
python main.py
```

### Using the Notebooks
Open the Jupyter notebooks in the Notebooks directory to explore the algorithm behavior and analysis.

## Algorithm Parameters

- **Alpha (α)**: Controls the influence of pheromone trails. Higher values make ants more likely to follow previously successful paths.
- **Beta (β)**: Controls the influence of distance. Higher values make ants prefer shorter edges.
- **Rho (ρ)**: Pheromone evaporation rate. Higher values cause faster forgetting of previous paths.
- **Q**: Pheromone deposit amount. Controls how much pheromone is deposited based on path quality.

## Results & Analysis

The notebooks include comparative analysis showing:
1. Convergence speed with different numbers of ants
2. Solution quality as a function of problem size
3. Visualization of pheromone concentration over time
4. Evolution of best and average path costs

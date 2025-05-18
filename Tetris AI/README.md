# Tetris AI

This project implements an AI agent that learns to play Tetris using a genetic algorithm. The AI evaluates moves based on a set of heuristics and evolves over generations to improve its performance.

## Features

- **Autonomous Tetris player**: The AI controls the falling pieces using heuristics and optimization.
- **Genetic Algorithm**:
  - Selection via tournament
  - Single-point crossover
  - Random mutation
- **Heuristic-based evaluation**: Each move is scored based on a weighted sum of features like line clears, holes, height, and blocking blocks.
- **Visualization**: Uses Pygame to render the Tetris gameplay.

## Files

- `tetris_ai.py`: Contains the core logic for the genetic algorithm and the AI gameplay loop.
- `tetris_base.py`: Provides game mechanics, rendering functions, and utilities. This is used as a base module by the AI.

## How It Works

1. A population of candidate solutions (chromosomes) is initialized with random weights.
2. Each chromosome plays a game, and its score is recorded.
3. The best-performing chromosomes are selected, crossed over, and mutated to form the next generation.
4. After a set number of generations, the best solution is used to run a final game with live visualization.

## Requirements

- Python 3
- Pygame

To install dependencies:

```bash
pip install pygame
```

## Running the AI

```bash
python tetris_ai.py
```

The program will train the AI over several generations and then display the best-performing agent in action.

## License

This project is open-source and available under the MIT License.
from tetris_ai import *
import random

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

def run_single_chromosome(chromosome, max, visualize=True, seed=42):
    random.seed(seed)
    if visualize:
         Score = run_ai_game(chromosome, max)
         print(Score)
    else:
        return evaluate_chromosome(chromosome)


chromosome = [-53.61353285108744, -79.79971411805417, -44.99413632617615, -55.35785237023545, 47.29424283280247, 35.33989748458225, 78.43591354096907, -82.61223347411678, -15.77137105734543]

run_single_chromosome(chromosome, max=600, visualize=True, seed=42)

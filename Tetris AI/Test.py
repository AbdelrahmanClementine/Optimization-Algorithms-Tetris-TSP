from Tetris_ai import *
import random

def run_single_chromosome(chromosome, visualize=True, seed=42):
    random.seed(seed)
    if visualize:
        num = run_ai_game(chromosome)  
        if num > 600 :
            print("WIN")
        else :
            print("LOSE")    
    else:
        return evaluate_chromosome(chromosome) 
    

chromosome =  [0.4729424283280248, 0.3533989748458226, 1.2085170054125585, 0.0549371543804511] 
run_single_chromosome(chromosome, visualize=True, seed=42)    

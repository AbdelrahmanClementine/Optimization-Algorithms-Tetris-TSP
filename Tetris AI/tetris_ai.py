import random
import time
import pygame
import sys
from pygame.locals import *
import tetris_base
import random

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

POPULATION_SIZE = 20
GENERATIONS = 30
MUTATION_RATE = 0.1
MUTATION_AMOUNT = 0.5

pygame.init()
tetris_base.FPSCLOCK = pygame.time.Clock()
tetris_base.DISPLAYSURF = pygame.display.set_mode((tetris_base.WINDOWWIDTH, tetris_base.WINDOWHEIGHT))
tetris_base.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
tetris_base.BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
pygame.display.set_caption('Tetris AI')


def create_chromosome():
    return [random.uniform(-1, 1) for _ in range(4)]

def evaluate_chromosome(chromosome):
    try:
        return run_ai_game(chromosome)
    except Exception as e:
        print(f"Game crashed with: {str(e)}")
        return 0  

def run_ai_game(chromosome):
    PieceNum = 0
    board = tetris_base.get_blank_board()
    score = 0
    falling_piece = tetris_base.get_new_piece()
    next_piece = tetris_base.get_new_piece()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        if not falling_piece:
            falling_piece = next_piece
            next_piece = tetris_base.get_new_piece()
            score += 1
            if not tetris_base.is_valid_position(board, falling_piece):
                return score

        initial_holes, initial_blocking = tetris_base.calc_initial_move_info(board)
        best_rot, best_x = select_best_move(board, falling_piece, initial_holes, initial_blocking, chromosome)
        falling_piece['rotation'] = best_rot
        falling_piece['x'] = best_x

        while tetris_base.is_valid_position(board, falling_piece, adj_Y=1):
            falling_piece['y'] += 1

        tetris_base.add_to_board(board, falling_piece)
        num_removed = tetris_base.remove_complete_lines(board)
        score += [0, 40, 120, 300, 1200][num_removed] if num_removed <=4 else 0

        tetris_base.DISPLAYSURF.fill(tetris_base.BGCOLOR)
        tetris_base.draw_board(board)
        tetris_base.draw_status(score, 1)
        tetris_base.draw_next_piece(next_piece)
        PieceNum+=1
        pygame.display.update()
        tetris_base.FPSCLOCK.tick(tetris_base.FPS)
        
        falling_piece = None
        
    return PieceNum


def select_best_move(board, piece, initial_holes, initial_blocking, chromosome):
    best_score = -float('inf')
    best_rot = 0
    best_x = 0
    original_state = {'rotation': piece['rotation'], 'x': piece['x'], 'y': piece['y']}

    for rotation in range(len(tetris_base.PIECES[piece['shape']])):
        piece['rotation'] = rotation
        min_x = -2  
        max_x = tetris_base.BOARDWIDTH - 1
        for x in range(min_x, max_x + 1):
            piece['x'] = x
            if tetris_base.is_valid_position(board, piece):
                temp_piece = {'shape': piece['shape'], 
                             'rotation': rotation,
                             'x': x,
                             'y': piece['y'],
                             'color': piece['color']}
                while tetris_base.is_valid_position(board, temp_piece, adj_Y=1):
                    temp_piece['y'] += 1
                
                if tetris_base.is_valid_position(board, temp_piece):
                    move_info = tetris_base.calc_move_info(board, temp_piece, x, rotation, 
                                                          initial_holes, initial_blocking)
                    if move_info[0]:
                        score = (chromosome[0] * move_info[2] +
                                chromosome[1] * (-move_info[3]) +
                                chromosome[2] * (-move_info[1]/10) +
                                chromosome[3] * (-move_info[4]))
                        if score > best_score:
                            best_score = score
                            best_rot, best_x = rotation, x

    piece.update(original_state)
    return best_rot, best_x



def select_parents(population, fitnesses):
    parents = []
    for _ in range(len(population)):
        tournament = random.sample(list(zip(population, fitnesses)), 3)
        parents.append(max(tournament, key=lambda x: x[1])[0])
    return parents

def crossover(p1, p2):
    point = random.randint(1, len(p1)-1)
    return p1[:point] + p2[point:]

def mutate(chromosome):
    return [gene + random.uniform(-MUTATION_AMOUNT, MUTATION_AMOUNT) 
            if random.random() < MUTATION_RATE else gene 
            for gene in chromosome]

def log_best_chromosomes(population, fitnesses, generation):
    paired = list(zip(population, fitnesses))
    paired.sort(key=lambda x: x[1], reverse=True)
    top2 = paired[:2]
    
    with open("log.txt", "a") as log_file:
        log_file.write(f"\nGeneration {generation}:\n")
        for i, (chrom, fit) in enumerate(top2, 1):
            log_file.write(f"  #{i} Chromosome: {chrom}, Score: {fit:.2f}\n")


def main():
    with open("log.txt", "w") as f:
        f.write("=== Tetris AI Genetic Algorithm Log ===\n")

    population = [create_chromosome() for _ in range(POPULATION_SIZE)]

    for gen in range(GENERATIONS):
        fitnesses = [evaluate_chromosome(c) for c in population]

        log_best_chromosomes(population, fitnesses, gen)

        paired = list(zip(population, fitnesses))
        paired.sort(key=lambda x: x[1], reverse=True)

        best_half = [chrom for chrom, _ in paired[:POPULATION_SIZE // 2]]

        print(f"Generation {gen}, Best: {paired[0][1]}, Avg: {sum(fitnesses)/len(fitnesses)}")

        parents = select_parents(population, fitnesses)
        new_half = []

        while len(new_half) < POPULATION_SIZE - len(best_half):
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1, p2)
            new_half.append(mutate(child))

        population = best_half + new_half

    final_fitnesses = [evaluate_chromosome(c) for c in population]
    best = max(zip(population, final_fitnesses), key=lambda x: x[1])[0]
    run_ai_game(best)

if __name__ == '__main__':
    main()

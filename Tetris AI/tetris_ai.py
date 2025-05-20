import random
import time
import pygame
import sys
from pygame.locals import *
import tetris_base
import random
import matplotlib.pyplot as plt

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

POPULATION_SIZE = 12
GENERATIONS = 10
MUTATION_RATE = 0.1
MUTATION_AMOUNT = 0.5

pygame.init()
tetris_base.FPSCLOCK = pygame.time.Clock()
tetris_base.DISPLAYSURF = pygame.display.set_mode((tetris_base.WINDOWWIDTH, tetris_base.WINDOWHEIGHT))
tetris_base.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
tetris_base.BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
pygame.display.set_caption('Tetris AI')


def create_chromosome():
    return [random.uniform(-100, 100) for _ in range(9)]


def evaluate_chromosome(chromosome):
    try:
        return run_ai_game(chromosome, 400)[0]
    except Exception as e:
        print(f"Game crashed with: {str(e)}")
        return 0


def run_ai_game(chromosome, max_pieces=999999999):
    piece_count = 0
    board = tetris_base.get_blank_board()
    score = 0
    falling_piece = tetris_base.get_new_piece()
    next_piece = tetris_base.get_new_piece()

    running = True  

    while running:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        if piece_count >= max_pieces:
            break  

        if not falling_piece:
            falling_piece = next_piece
            next_piece = tetris_base.get_new_piece()
            piece_count += 1
            if not tetris_base.is_valid_position(board, falling_piece):
                break

        initial_holes, initial_blocking = tetris_base.calc_initial_move_info(board)
        best_rot, best_x = select_best_move(board, falling_piece, initial_holes, initial_blocking, chromosome)
        falling_piece['rotation'] = best_rot
        falling_piece['x'] = best_x

        while tetris_base.is_valid_position(board, falling_piece, adj_Y=1):
            falling_piece['y'] += 1

        tetris_base.add_to_board(board, falling_piece)
        num_removed = tetris_base.remove_complete_lines(board)
        score += [0, 40, 120, 300, 1200][num_removed] if num_removed <= 4 else 0

        tetris_base.DISPLAYSURF.fill(tetris_base.BGCOLOR)
        tetris_base.draw_board(board)
        tetris_base.draw_status(score, 1)
        tetris_base.draw_next_piece(next_piece)
        pygame.display.update()
        tetris_base.FPSCLOCK.tick(tetris_base.FPS)

        falling_piece = None

    return score , piece_count  


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
                    
                    move_info2 = tetris_base.calc_initial_move_info(board)

                    if move_info[0]:
                        score = (chromosome[0] * (move_info[2]) +
                                 chromosome[1] * (move_info[3]) +
                                 chromosome[2] * (move_info[1]) +
                                 chromosome[3] * (move_info[4]) + 
                                 chromosome[4] * (move_info[5]) +
                                 chromosome[5] * (move_info[6]) +
                                 chromosome[6] * (move_info[7]) + 
                                 chromosome[7] * (move_info2[0])+ 
                                 chromosome[8] * (move_info2[1]))
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
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:]


def mutate(chromosome):
    return [gene + random.uniform(-MUTATION_AMOUNT, MUTATION_AMOUNT)
            if random.random() < MUTATION_RATE else gene
            for gene in chromosome]


best_scores_over_gens = []


def log_best_chromosomes(population, fitnesses, generation):
    paired = list(zip(population, fitnesses))
    paired.sort(key=lambda x: x[1], reverse=True)
    top2 = paired[:2]

    with open("log.txt", "a") as log_file:
        if generation == 0:
            log_file.write("=== Genetic Algorithm Configuration ===\n")
            log_file.write(f"Number of GENERATIONS Used: {GENERATIONS}\n")
            log_file.write(f"POPULATION_SIZE Used: {POPULATION_SIZE}\n")
            log_file.write(f"MUTATION_RATE Used: {MUTATION_RATE}\n")
            log_file.write(f"Random Seed Used: {RANDOM_SEED}\n")
            log_file.write("Contribution Factors (chromosome genes):\n")
            log_file.write("  [0] max_height            - Height of the tallest column\n")
            log_file.write("  [1] num_removed_lines     - Number of lines cleared after placing a piece\n")
            log_file.write("  [2] new_holes             - New holes created by the latest piece\n")
            log_file.write("  [3] new_blocking_blocks   - New blocks that may block existing holes\n")
            log_file.write("  [4] piece_sides           - Number of sides of the piece touching other blocks\n")
            log_file.write("  [5] floor_sides           - Number of sides of the piece touching the floor\n")
            log_file.write("  [6] wall_sides            - Number of sides of the piece touching the wall\n")
            log_file.write("  [7] total_holes           - Number of empty cells with filled cells above them\n")
            log_file.write("  [8] total_blocking_blocks - Number of blocks sitting above holes\n")
            log_file.write("=========================================\n")

        log_file.write(f"\nGeneration {generation}:\n")
        for i, (chrom, fit) in enumerate(top2, 1):
            log_file.write(f"  #{i} Chromosome: {chrom}, Score: {fit:.2f}\n")

    best_scores_over_gens.append([top2[0][1], top2[1][1]])


def plot_best_chromosomes():
    gens = list(range(1, GENERATIONS + 1))
    best1 = [scores[0] for scores in best_scores_over_gens]
    best2 = [scores[1] for scores in best_scores_over_gens]

    plt.figure(figsize=(10, 5))
    plt.plot(gens, best1, label='Best Chromosome', marker='o')
    plt.plot(gens, best2, label='Second Best Chromosome', marker='x')
    plt.title('Best Two Chromosomes Across Generations')
    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("best_chromosomes_plot.png")  
    plt.show()



def main():
    pygame.init()
    with open("log.txt", "w") as f:
        f.write("=== Tetris AI Genetic Algorithm Log ===\n")

    population = [create_chromosome() for _ in range(POPULATION_SIZE)]

    for gen in range(GENERATIONS):
        fitnesses = [evaluate_chromosome(c) for c in population]

        log_best_chromosomes(population, fitnesses, gen)

        paired = list(zip(population, fitnesses))
        paired.sort(key=lambda x: x[1], reverse=True)

        best_half = [chrom for chrom, _ in paired[:POPULATION_SIZE // 2]]

        print(f"Generation {gen}, Best: {paired[0][1]}, Avg: {sum(fitnesses) / len(fitnesses)}")

        parents = select_parents(population, fitnesses)
        new_half = []

        while len(new_half) < POPULATION_SIZE - len(best_half):
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1, p2)
            new_half.append(mutate(child))

        population = best_half + new_half

    final_fitnesses = [evaluate_chromosome(c) for c in population]
    best = max(zip(population, final_fitnesses), key=lambda x: x[1])[0]
    run_ai_game(best, 400)
    pygame.quit()

    plot_best_chromosomes()


if __name__ == '__main__':
    main()

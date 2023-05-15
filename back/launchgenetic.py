from genetic.model.geneticalgorithm import GeneticAlgorithm
from genetic.model.chromosome import Chromosome
from model.game_manager import GameManager
from model.mtcs.splendia_mtcs_node import SplendiaMtcsNode


import math

# The evaluation function for the board position


def evaluate(board: SplendiaMtcsNode, gene: Chromosome):
    total_tokens = board
    # Your evaluation function here
    return 0

# The Alpha-Beta algorithm


def alpha_beta(board: SplendiaMtcsNode, depth: int, alpha: float, beta: float, maximizing_player: bool, gene):
    if depth == 0 or (board.is_last_turn()):
        return evaluate(board, gene)
    board.find_children()
    if maximizing_player:
        max_eval = -math.inf
        for move in (board.child):
            eval = alpha_beta(move, depth - 1, alpha, beta, False)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for move in (board.child):
            eval = alpha_beta(move, depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def splendor_battle(gene1: Chromosome, gene2: Chromosome):
    first_state = GameManager(nbPlayer=2)
    node: SplendiaMtcsNode = SplendiaMtcsNode(first_state, 2, 0, False, 9)
    # find best move with alpha beta
    while not node.is_last_turn():
        node.find_children()
        if node.currentPlayer == 0:
            alpha_beta(node, 2, -math.inf, math.inf, True, gene1)


"""genetic_algorithm = GeneticAlgorithm(3, 0.2, 0.1, 10000, lambda x: sum(x), lambda population, n: population[:n])
genetic_algorithm.run()"""
def fitness_function(x): return sum(x)
def selection_function(population, n): return population[:n]


genetic_algorithm = GeneticAlgorithm(
    1000, 0.8, 0.01, 1000, fitness_function, selection_function)
best_individual = genetic_algorithm.run()

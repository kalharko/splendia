import random
from typing import List, Tuple, Callable


class Chromosome:
    def __init__(self, genes: List[int]):
        self.genes = genes
        self.fitness = 0.0
        self.winrate = 0.0

    def calculate_fitness(self, fitness_function: Callable[[List[int]], float]) -> float:
        self.fitness = fitness_function(self.genes)
        return self.fitness

    def crossover(self, other: 'Chromosome', crossover_rate: float) -> Tuple['Chromosome', 'Chromosome']:
        if random.random() >= crossover_rate:
            return self, other

        # Perform crossover operation
        crossover_point = random.randint(0, len(self.genes) - 1)
        child_1 = Chromosome(
            self.genes[:crossover_point] + other.genes[crossover_point:])
        child_2 = Chromosome(
            other.genes[:crossover_point] + self.genes[crossover_point:])
        return child_1, child_2

    def mutate(self, mutation_rate: float) -> 'Chromosome':
        for i in range(len(self.genes)):
            if random.random() < mutation_rate:
                # Flip the bit
                self.genes[i] = 1 - self.genes[i]
        return self

    def __str__(self) -> str:
        return f"Chromosome: {self.genes}, Fitness: {self.fitness:.2f}"

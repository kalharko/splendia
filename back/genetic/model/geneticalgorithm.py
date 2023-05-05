from genetic.model.chromosome import Chromosome
from typing import List, Callable
import random
class GeneticAlgorithm:
    def __init__(self, population_size: int, crossover_rate: float, mutation_rate: float, generations: int,
                 fitness_function: Callable[[List[int]], float], selection_function: Callable[[List[Chromosome], int], List[Chromosome]]):
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.fitness_function = fitness_function
        self.selection_function = selection_function
        self.population = [Chromosome([random.randint(0, 1) for _ in range(10)]) for _ in range(population_size)]


    def run(self) -> Chromosome:
        for generation in range(self.generations):
            # Calculate fitness for each individual
            for individual in self.population:
                individual.calculate_fitness(self.fitness_function)

            # Sort the population by fitness
            self.population.sort(key=lambda x: x.fitness, reverse=True)

            # Print the best individual in the current generation
            print(f"Generation {generation + 1}: Best Fitness = {self.population[0].fitness:.2f}, Best Chromosome = {self.population[0].genes}")

            # Check if we've reached the stopping criteria (e.g. target fitness)
            if self.population[0].fitness >= 10.0:
                return self.population[0]

            # Select individuals for the next generation
            selected_population = self.selection_function(self.population, self.population_size)

            # Create new population through crossover and mutation
            new_population = []
            for i in range(0, self.population_size, 2):
                parent_1, parent_2 = selected_population[i], selected_population[i+1]
                child_1, child_2 = parent_1.crossover(parent_2, self.crossover_rate)
                new_population.append(child_1.mutate(self.mutation_rate))
                new_population.append(child_2.mutate(self.mutation_rate))

            # Replace the old population with the new population
            self.population = new_population

        # Return the best individual found
        return self.population[0]


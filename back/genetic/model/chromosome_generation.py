from genetic.model.chromosome import Chromosome
import pickle

class ChromosomeGeneration:
    def __init__(self, generation_num):
        self.generation_num = generation_num
        self.chromosomes = []
        self.best_result = 0
        self.goal_reached = False

    def add_chromosome(self, chromosome):
        self.chromosomes.append(chromosome)

    def set_chromosomes(self, chromosomes):
        self.chromosomes = chromosomes
        self.get_best_result()

    def get_best_result(self):
        self.best_result = self.chromosomes[0].fitness
        return self.best_result


    # def set_fitness(self, fitness_scores):
    #     for i, chromosome in enumerate(self.chromosomes):
    #         chromosome.fitness = fitness_scores[i]
        
    def print_chromosome_generation(self):
        self.chromosomes.sort(key=lambda chromosome: chromosome.fitness, reverse=True)
        print("=====================================")
        print("Génération n°", {self.generation_num})
        self.best_result = self.chromosomes[0].fitness
        print("Best result :" , self.best_result)
        print("=====================================")
        for index, chromosome in zip(range(5),self.chromosomes):
            print("n°",index, " : ", chromosome)
        print("=====================================")

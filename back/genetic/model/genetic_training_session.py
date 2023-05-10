from genetic.model.chromosome_generation import ChromosomeGeneration
import pickle
from typing import List

class GeneticTrainingSession:
    def __init__(self):
        self.generations_list: List[ChromosomeGeneration] = []
        self.best_result: int = 0
        self.best_index: int = 0
        self.goal_reached: bool = False
    
    def load_training_session(self):
        with open("genetic\model\chromosomes_generations.pkl", "rb") as f:
            saved_training_session = pickle.load(f)
            if saved_training_session:
                self.generations_list = saved_training_session.generations_list
                self.best_index = saved_training_session.best_index
                self.best_result = saved_training_session.best_result
                self.goal_reached = saved_training_session.goal_reached
            else:
                print("No training session saved yes, please run the genetic algorithm first")
                exit()

               

    def append_chromosome_generation(self, chromosome_generation: ChromosomeGeneration):
        self.generations_list.append(chromosome_generation)

    def print_training_session(self):
        self.load_training_session(self)
        for chromosome_generation in self.generations_list:
            chromosome_generation.print_chromosome_generation()
        print("=====================================")
        print("Best result : ", self.best_result)
        print("=====================================")
        print("Best index : ", self.best_index)
        print("=====================================")
        print("Goal reached : ", self.goal_reached)
        print("=====================================")

    def delete_training_session(self):
        with open("genetic\model\chromosomes_generations.pkl", "wb") as f:
            pickle.dump([], f)
        return True
    
    def save_training_session(self):
        self.best_index, best_generation = max(enumerate(self.generations_list), key=lambda x: x[1].best_result)
        self.best_result = best_generation.best_result
        with open("genetic\model\chromosomes_generations.pkl", "wb") as f:
            pickle.dump(self, f)
        return True
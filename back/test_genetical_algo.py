from genetic.model.genetic_algorithm import GeneticAlgorithm
from genetic.model.genetic_training_session import GeneticTrainingSession

def generate_chromosome():
    average_generation : int = 0
    fitness_function = lambda x: sum(x)
    selection_function = lambda population, n: population[:n]


    # for i in range(10):
    #     crossover_rate = i/10
    #     genetic_algorithm = GeneticAlgorithm(100, crossover_rate, 0.1, 100, fitness_function, selection_function)
    #     for i in range(1000):
    #         last_generation = genetic_algorithm.run()
    #         average_generation += last_generation
    #     average_generation /= 100
    #     print(f"Average generation for crossover rate {crossover_rate}: {average_generation}")

    genetic_algorithm = GeneticAlgorithm(1000, 0.6, 0.1, 100, fitness_function, selection_function)
    goal_reached = genetic_algorithm.run()
    print(f"goal reached, {goal_reached}")


def ask_for_action():
    action = input("What do you want to do ?\n 1 - Generate a chromosome\n 2 - Print the chromosome generations\n 3 - Delete the chromosome generations\n")
    if action == "1":
        generate_chromosome()
    elif action == "2":
        GeneticTrainingSession.print_training_session(GeneticTrainingSession)
    elif action == "3":
        GeneticTrainingSession.delete_training_session(GeneticTrainingSession)
    else:
        print("Please enter a valid action")
        ask_for_action()
    return action

if __name__ == "__main__":
    ask_for_action()

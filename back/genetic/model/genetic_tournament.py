from genetic.model.chromosome import Chromosome
from genetic.model.duel import Duel
from typing import List


class GeneticTournament:
    def __init__(self, population : List[Chromosome], games_by_duels: int = 10):
        self.population : List[Chromosome] = population
        self.games_by_duels = games_by_duels
        self.duels : List[Duel] = []

    # def select(self):
    #     tournament = []
    #     for i in range(self.tournament_size):
    #         tournament.append(self.population[random.randint(0, len(self.population) - 1)])
    #     return max(tournament, key=lambda x: x.fitness)

    def start_tournamenent(self):
        for chromosome in self.population:
            chromosome.fitness = 0
        for i in range(len(self.population)):
            for j in range(i+1, len(self.population)):
                if i != j:
                    if self.population[i] is not None and self.population[j] is not None:
                        duel = Duel(self.population[i], self.population[j], self.games_by_duels).start_duel()
                        self.duels.append(duel)
        return self.get_tournament_winner()
    

    def get_tournament_winner(self):
        for rank, chromosome in enumerate(self.population):
            # for duel in chromosome.duel_list:
            #     if duel.chromosome1 == chromosome:
            #         win_count += duel.chromosome1_win
            #     else:
            #         win_count += duel.chromosome2_win
            chromosome.fitness = chromosome.winrate / chromosome.game_count
            print("chromosome", rank ,"fitness : ", chromosome.fitness)
        return max(self.population, key=lambda x: x.fitness)
    
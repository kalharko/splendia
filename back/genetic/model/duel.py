from genetic.model.chromosome import Chromosome

class Duel:

    def __init__(self, chromosome1: Chromosome, chromosome2: Chromosome, games_by_duels : int) -> None:
        self.chromosome1 : Chromosome = chromosome1
        self.chromosome2 : Chromosome = chromosome2
        self.games_by_duels : int = games_by_duels
        self.chromosome1_win : int = 0
        self.chromosome2_win : int = 0
        chromosome1.duel_list.append(self)
        chromosome2.duel_list.append(self)
    
    def start_duel(self):
        for i in range(self.games_by_duels):
            self.chromosome1_win += self.chromosome1.duel(self.chromosome2)
        self.chromosome1.winrate += self.chromosome1_win
        self.chromosome2.winrate += self.games_by_duels - self.chromosome1_win



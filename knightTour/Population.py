from Knight import Knight
import random

class Population:
    def __init__(self, population_size):
        self.population_size = population_size
        self.generation = 1
        self.knights = [Knight() for _ in range(self.population_size)]

    def check_population(self):
        for knight in self.knights:
            knight.check_moves()

    def evaluate(self):
        best_solution = 0
        for knight in self.knights:
            eval = knight.evaluate_fitness()
            if eval > best_solution :
                best_knight = knight
                best_solution = eval
                #best_solution = eval 
        return best_knight.fitness,best_knight

    def tournament_selection(self, size=3):
        tournament_sample = random.sample(self.knights, size)
        winner1 = max(tournament_sample, key=lambda knight: knight.fitness)
        tournament_sample.remove(winner1)
        winner2 = max(tournament_sample, key=lambda knight: knight.fitness)
        return winner1, winner2

    def create_new_generation(self):
        new_generation = []


        for _ in range(self.population_size // 2): # si population_size = 30, on aura besoin que de 15 generation car on genere a chaque fois 2 offprings
            parent1, parent2 = self.tournament_selection()
            offspring1, offspring2 = parent1.chromosome.crossover(parent2.chromosome)
            offspring1.mutation()
            offspring2.mutation()
            knight1 = Knight(chromosome=offspring1)
            knight2 = Knight(chromosome=offspring2)
            new_generation.append(knight1)
            new_generation.append(knight2)


        self.knights = new_generation
        self.generation += 1


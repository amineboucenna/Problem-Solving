import random

class Chromosome:
    def __init__(self, genes=None):
        if genes is None:
            self.genes = self.generate_random_genes()
        else:
            self.genes = genes

    def generate_random_genes(self):
        return [random.randint(1, 8) for _ in range(63)]

    def crossover(self, partner):
        crossover_point = random.randint(1, len(self.genes) - 1)
        new_genes1 = self.genes[:crossover_point] + partner.genes[crossover_point:]
        new_genes2 = partner.genes[:crossover_point] + self.genes[crossover_point:]

        offspring1 = Chromosome(genes=new_genes1)
        offspring2 = Chromosome(genes=new_genes2)

        return offspring1, offspring2


    def mutation(self):
        for i in range(63):
            if random.random() < 0.01:
                self.genes[i] = random.randint(1, 8)

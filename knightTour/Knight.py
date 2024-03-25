from Chromosome import Chromosome
import random

class Knight:
    def __init__(self, chromosome=None):
        self.path = []
        if chromosome is None:
            self.chromosome = Chromosome()
        else:
            self.chromosome = chromosome
        self.position = (0, 0)
        self.fitness = 0
        self.path.append(self.position)
      
    
    def move_forward(self, direction):
        line, column = self.position
        new_line, new_column = line,column
        # On a utilisé les meme directions que le tp
        match direction:
            case 1:
                new_line, new_column = line - 1, column + 2
            case 2:
                new_line, new_column = line - 2, column + 1
            case 3:
                new_line, new_column = line + 1, column + 2
            case 4:
                new_line, new_column = line + 2, column + 1
            case 5:
                new_line, new_column = line + 2, column - 1
            case 6:
                new_line, new_column = line + 1, column - 2
            case 7:
                new_line, new_column = line - 1, column - 2
            case 8:
                new_line, new_column = line - 2, column - 1

        self.position = (new_line, new_column)
        return direction



    def move_backward(self, direction):
        line, column = self.position
        new_line, new_column = line,column
        match direction:
            case 1:
                new_line, new_column = line + 1, column - 2
            case 2:
                new_line, new_column = line + 2, column - 1
            case 3:
                new_line, new_column = line - 1, column - 2
            case 4:
                new_line, new_column = line - 2, column - 1
            case 5:
                new_line, new_column = line - 2, column + 1
            case 6:
                new_line, new_column = line - 1, column + 2
            case 7:
                new_line, new_column = line + 1, column + 2
            case 8:
                new_line, new_column = line + 2, column + 1

        self.position = (new_line, new_column)
        return direction

    def check_moves(self):
        for i, move in enumerate(self.chromosome.genes):
            forward = self.move_forward(move)

            if not self.is_move_valid():
                self.move_backward(forward)

                cycle_type = random.choice([1, 2])  # 1: normal cycle | 2: backward cycle
                updated = False
                index = forward
                for _ in range(8): 
                    if cycle_type == 1:
                        if index == 8 : 
                            index = 1
                        else:    
                            index+=1
                    else:
                        if index == 1:
                            index=8
                        else:
                            index-=1

                    self.move_forward(index)
                    if self.is_move_valid():
                        self.chromosome.genes[i] = index
                        self.path.append(self.position)
                        break
                    else:
                        self.move_backward(index)

                #if not updated:  # on a essayé de faire tout, mais toujours ne marche pas alors on le garde
                #   self.move_forward(forward)
                #    self.chromosome.genes[i] = move
                    #self.path.append(self.position) 
                    #self.move_backward(forward)
            else:
                # move is valid add it to the path.
                self.path.append(self.position)


    def evaluate_fitness(self):
        for position in self.path:
            line , column = position
            if 0 <= line < 8 and 0 <= column < 8 :
                self.fitness += 1
            else:
                break

        return self.fitness

    def is_move_valid(self):
        line, column = self.position
        return 0 <= line < 8 and 0 <= column < 8 and self.position not in self.path

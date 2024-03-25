from copy import deepcopy
import pandas as pd
import csv

class Fifteenpuzzle:    

    def __init__(self, puzzle_file):         
        # Initialize the Fifteenpuzzle Board
        self.board = [['' for _ in range(4)] for _ in range(4)]
        # i want to read the board from the scv file # board.csv
        self.board_height,self.board_width = 4,4
        self.setBoard(puzzle_file)


    def setBoard(self,puzzle_file):
        i,j=0,0

        csv_content = pd.read_csv(puzzle_file,delimiter=',')

        for line in csv_content:
            self.board[j][i] = line
            i+=1
            if i==4:
                i=0
                j+=1

    @staticmethod
    def printBoard(board):
        for y in range(4):
            print("---------------")
            print(f"| {board[y][0]} | {board[y][1]} | {board[y][2]} | {board[y][3]}|")

    def isGoal(self):
        goal_board = [['13','14','15',' '],['9','10','11','12'],['5','6','7','8'],['1','2','3','4']]


        if self.board == goal_board:
            return True
        return False     
    
    # Generate the successors
    def successorFunction(self):
        succs = list()
        # L:Left
        # R:Right
        # U:Up
        # D:Down
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == ' ':
                    if x+1 < 4 :#LEFT
                        successor = deepcopy(self)
                        successor.board[y][x] = self.board[y][x+1]
                        successor.board[y][x+1] = ' '
                        succs.append(("{}:L".format(successor.board[y][x]), successor))
                    if x-1 >= 0 :#RIGHT
                        successor = deepcopy(self)
                        successor.board[y][x] = self.board[y][x-1]
                        successor.board[y][x-1] = ' '
                        succs.append(("{}:R".format(successor.board[y][x]), successor))
                    if y-1 >= 0 :#UP
                        successor = deepcopy(self)
                        successor.board[y][x] = self.board[y-1][x]
                        successor.board[y-1][x] = ' '
                        succs.append(("{}:U".format(successor.board[y][x]), successor))
                    if y+1 < 4 :#DOWN
                        successor = deepcopy(self)
                        successor.board[y][x] = self.board[y+1][x]
                        successor.board[y+1][x] = ' '
                        succs.append(("{}:D".format(successor.board[y][x]), successor))

        return succs


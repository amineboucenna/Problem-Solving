from copy import deepcopy
import pandas as pd
from queue import PriorityQueue

class FifteenPuzzle:    

    def __init__(self, puzzle_file):         
        # Initialize the FifteenPuzzle Board
        self.board = [[0 for _ in range(4)] for _ in range(4)]
        # Read the board from the CSV file (board.csv)
        self.board_height, self.board_width = 4, 4
        self.set_board(puzzle_file)

    def set_board(self, puzzle_file):
        csv_content = pd.read_csv(puzzle_file, delimiter=',', header=None)

        for i in range(4):
            for j in range(4):
                cell_value = csv_content.iloc[i, j]
                self.board[i][j] = int(cell_value) if cell_value != ' ' else 0

    @staticmethod
    def print_board(board):
        for y in range(4):
            print("---------------")
            print(f"| {board[y][0]:<2} | {board[y][1]:<2} | {board[y][2]:<2} | {board[y][3]:<2} |")

    def is_goal(self):
        goal_state = [[13, 14, 15, 0],[9, 10, 11, 12],[5, 6, 7, 8],[1, 2, 3, 4] ]

        # Compare each element of the board with the corresponding element in the goal state
        for i in range(4):
            for j in range(4):
                if self.board[i][j] != goal_state[i][j]:
                    return False

        return True
    
    # Generate the successors
    def successor_function(self):
        succs = list()
        # L: Left, R: Right, U: Up, D: Down
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 0:
                    # DOWN
                    if y + 1 < 4:
                        successor = deepcopy(self)
                        successor.board[y][x] = self.board[y + 1][x]
                        successor.board[y + 1][x] = 0
                        succs.append(("{}:D".format(successor.board[y][x]), successor))
                    if x + 1 < 4:  # LEFT
                        successor = deepcopy(self)
                        successor.board[y][x] = self.board[y][x + 1]
                        successor.board[y][x + 1] = 0
                        succs.append(("{}:L".format(successor.board[y][x]), successor))
                    if y - 1 >= 0:  # UP
                        successor = deepcopy(self)
                        successor.board[y][x] = self.board[y - 1][x]
                        successor.board[y - 1][x] = 0
                        succs.append(("{}:U".format(successor.board[y][x]), successor))
                    if x - 1 >= 0:  # RIGHT
                        successor = deepcopy(self)
                        successor.board[y][x] = self.board[y][x - 1]
                        successor.board[y][x - 1] = 0
                        succs.append(("{}:R".format(successor.board[y][x]), successor))
                    


        return succs

class Node:

    def __init__(self, fifteen_puzzle, parent=None, action="", c=1, heuristic=1):
        self.state = fifteen_puzzle
        self.parent = parent
        self.action = action
        self.g = 0 if not self.parent else self.parent.g
        self.set_f(heuristic)

    def set_f(self, heuristic): 
        heuristics = {1: self.heuristic1()}
        self.f = self.g + heuristics[heuristic]

    def __lt__(self, other):
        return self.f >= other.f

    def heuristic1(self):
        goal_state = [[13, 14, 15, 0],[9, 10, 11, 12],[5, 6, 7, 8],[1, 2, 3, 4] ]
        count = 0
        for i in range(4):
            for j in range(4):
                if self.state.board[i][j] == goal_state[i][j]:
                    count += 1
        return count
    
    def get_path(self):
        states = []
        node = self
        while node is not None:
            states.append(node.state)
            node = node.parent
        return states[::-1]

    def get_solution(self):
        actions = []
        node = self
        while node is not None:
            actions.append(node.action)
            node = node.parent
        return actions[::-1]

class Search:
    """ Astar Search """
    @staticmethod
    def astar(initial_state):
        initial_node = Node(initial_state)
        initial_node.g = 0
        initial_node.f = initial_node.heuristic1()


        # Create the OPEN priority queue and the CLOSED list
        open = PriorityQueue()  # A priority queue
        open.put((initial_node.f,initial_node))
        closed = []

        step = 0
        while True:
            #print(f'*** Step {step} ***')

            if open.empty():
                return None, step

            current = open.get()[1]
            if current.state.is_goal():
                print("Goal reached")
                return current, step

            closed.append(current)

            step += 1
            for (action, successor) in current.state.successor_function():
                child = Node(successor, current, action)
                child.g = current.g + 1
                child.f = child.g + current.heuristic1()

                if (child.state.board not in [node.state.board for node in closed] and \
                        child.state.board not in [node[1].state.board for node in list(open.queue)]):
                    open.put((child.f,child))
                elif any(child.state.board == node[1].state.board and node[1].f > child.f for node in list(open.queue)):
                    temp_open = PriorityQueue()

                    [temp_open.put((child.f, child)) if node[1].state.board == child.state.board else temp_open.put(
                        (node[0], node[1])) for node in list(open.queue)]

                    open = temp_open
                elif any( node.state.board == child.state.board and node.f is not None and node.f > child.f for node in closed):
                    node_reference = next((i for i, node in enumerate(closed) if
                                            node.state.board == child.state.board and node.f is not None and node.f > child.f))
                    closed.pop(node_reference)
                    open.put((child.f,child))
def main():
    initial_state = FifteenPuzzle('board3.csv')
    FifteenPuzzle.print_board(initial_state.board)
    goal_node, step = Search.astar(initial_state)
    if goal_node:
        print(f"Number of steps: {step}")
        print("Moves: {}".format(" ".join(map(str, goal_node.get_solution()))))
    else:
        print("No solution")

if __name__ == "__main__":
    main()

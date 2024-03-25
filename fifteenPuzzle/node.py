class Node:

    def __init__(self, fifteenpuzzle, parent=None, action="", c=1, heuristic=1):
        self.state = fifteenpuzzle
        self.parent = parent
        self.action = action
        self.g = 0 if not self.parent else self.parent.g + c
        self.setF(heuristic)

    def setF(self, heuristic): #number of cases in their position
        heuristics = {1: self.heuristic1()
                      }
        self.f = self.g + heuristics[heuristic]

    def __lt__(self, other):
        return self.f < other.f

    def heuristic1(self):
        goal_state = [
        [1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15, ]
    ]

        count = 0
        for i in range(4):
            for j in range(4):
                if self.state.board[i][j] == goal_state[i][j]:
                    count += 1
        return count


    def getPath(self):
        states = []
        node = self
        while node != None:
            states.append(node.state)
            node = node.parent
        return states[::-1]
    
    def getSolution(self):
        actions = []
        node = self
        while node != None:
            actions.append(node.action)
            node = node.parent
        return actions[::-1]

            




class Node:

    def __init__(self, rushHourPuzzle, parent=None, action="", c=1, heuristic=1):
        self.state = rushHourPuzzle
        self.parent = parent
        self.action = action
        self.g = 0 if not self.parent else self.parent.g + c
        self.setF(heuristic)   

    # Choose one of the available heuristics
    def setF(self, heuristic):
        heuristics = {1: self.heuristic1(),
                    2: self.heuristic2()}
        self.f = self.g + heuristics[heuristic]

    def __lt__(self, other):
        return self.f < other.f

    """ First heuristic: Distance from target vehicle to the exit """
    def heuristic1(self):
        for vehicle in self.state.vehicles:
            if vehicle["id"] == 'X':
                return int(self.state.board_width-2-vehicle["x"])
    
    """ Second heuristic: number of vehicles that block the way to the exit """
    def heuristic2(self):
        for vehicle in self.state.vehicles:
            if vehicle["id"] == 'X':
                unique_vehicles = set(self.state.board[vehicle["y"]][vehicle["x"]:])
                if ' ' in unique_vehicles:
                    return self.heuristic1()+len(unique_vehicles)-2
                return self.heuristic1()+len(unique_vehicles)-1
            
    """ Third heuristic:  number of walls in front of a vehicle """
    def heuristic3(self):
        sum_walls = 0

        for vehicle in self.state.vehicles:

            if vehicle["orientation"] == 'H':
                for x in range(vehicle["x"] + vehicle["length"], self.state.board_width):
                    if (x, vehicle["y"]) in self.state.walls:
                        sum_walls += 1
                for x in range(vehicle["x"] - 1, 0, -1):
                    if (x, vehicle["y"]) in self.state.walls:
                        sum_walls += 1
            else: 
                for y in range(vehicle["y"] + vehicle["length"], self.state.board_height):
                    if (vehicle["x"], y) in self.state.walls:
                        sum_walls += 1
                for y in range(vehicle["y"] - 1, 0, -1):
                    if (vehicle["x"], y) in self.state.walls:
                        sum_walls += 1

        return self.heuristic2() + sum_walls

    """ 4 """
    def heuristic4(self):
        return self.heuristic1() + self.heuristic2()
    
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

            




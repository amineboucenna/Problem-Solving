from node import Node
from queue import Queue,PriorityQueue
from rushHourPuzzle import RushHourPuzzle
class Search:

    """ Uninformed/Blind Search """
    @staticmethod
    def breadthFirst(initial_state):
        
        initial_node = Node(initial_state)   
        # Check if the start element is the goal
        if initial_node.state.isGoal():
            return initial_node, 0

        # Create the OPEN FIFO queue and the CLOSED list
        open = Queue() # A FIFO queue
        open.put(initial_node)
        closed = list()
       
        step = 0
        while True:
            print (f'*** Step {step} ***')
            # Check if the OPEN queue is empty => goal not found 
            if open.empty():
                return None, step            
            # Get the first element of the OPEN queue
            current = open.get()            
            # Put the current node in the CLOSED list
            closed.append(current)
            step +=1 
            # Generate the successors of the current node
            for (action, successor) in current.state.successorFunction():                
                child = Node(successor, current, action)
                # Check if the child is not in the OPEN queue and the CLOSED list
                if (child.state.board not in [node.state.board for node in closed] and \
                    child.state.board not in [node.state.board for node in list(open.queue)]):
                    # Check if the child is the goal
                    if child.state.isGoal():
                        print ("Goal reached")
                        return child, step 
                    # Put the child in the OPEN queue 
                    open.put(child)

    """ Astar Search """
    @staticmethod
    def Astar(initial_state):
        initial_node = Node(initial_state)
        initial_node.g = 0
        initial_node.f = initial_node.heuristic3()


        # Create the OPEN priority queue and the CLOSED list
        open = PriorityQueue()  # A priority queue
        open.put((initial_node.f,initial_node))
        closed = []

        step = 0
        while True:
            print(f'*** Step {step} ***')

            if open.empty():
                return None, step

            current = open.get()[1]
            if current.state.isGoal():
                print("Goal reached")
                return current, step

            closed.append(current)

            step += 1
            for (action, successor) in current.state.successorFunction():
                child = Node(successor, current, action)
                child.g = current.g + 1
                child.f = child.g + current.heuristic3()

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

    initial_state = RushHourPuzzle('1.csv')
    RushHourPuzzle.printRushHourBoard(initial_state.board)
    #goal_node, step = Search.breadthFirst(initial_state)
    goal_node, step = Search.Astar(initial_state)

    print(f"Path cost: {goal_node.g}")
    print(f"Number of steps: {step}")
    print("Moves: {}".format(" ".join(map(str, goal_node.getSolution()))))

if __name__ == "__main__":
    main()
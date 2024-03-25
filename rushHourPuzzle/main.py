from search import Search
from rushHourPuzzle import RushHourPuzzle
import pygame
from time import sleep

colors = ["orange", "green", "purple", "yellow", "blue", "cyan", "pink", "brown"]
BORDER = (200, 200, 200)
WINDOW_HEIGHT = 600
WINDOW_WIDTH = 600

def drawGrid(initial_state):
    
    blockSize_w = int(WINDOW_WIDTH / initial_state.board_width)
    blockSize_h = int(WINDOW_HEIGHT / initial_state.board_height)

    for x in range(0, WINDOW_WIDTH, blockSize_w):
        for y in range(0, WINDOW_HEIGHT, blockSize_h):
            rect = pygame.Rect(x, y, blockSize_w, blockSize_h)
            pygame.draw.rect(screen, BORDER, rect, 2)

    for y in range(initial_state.board_height):
        for x in range(initial_state.board_width):
            if initial_state.board[y][x] == "#":
                wall_image = pygame.image.load("wall.png")
                wall_image = pygame.transform.scale(wall_image, (blockSize_w, blockSize_h))
                screen.blit(wall_image, pygame.Rect(x*blockSize_w,y*blockSize_h,blockSize_w,blockSize_h))
            elif initial_state.board[y][x] != ' ':
                car_id = initial_state.board[y][x]
                car = None


                for pos,vehicle in enumerate(initial_state.vehicles):
                    if vehicle["id"] == car_id:
                        if vehicle["id"] == 'X':
                            vehicle["color"] = "red"
                        else:
                            vehicle["color"] = colors[pos % len(colors)]
                        car = vehicle
                        break

                if car is not None:
                    car_rect = pygame.Rect(
                        x * blockSize_w,
                        y * blockSize_h,
                        (car["length"]-1) * blockSize_w if car["orientation"] == 'H' else blockSize_w,
                        blockSize_h if car["orientation"] == 'V' else blockSize_h
                    )
                    pygame.draw.rect(screen, car["color"], car_rect)


def make_move(initial_state, vehicle_id, move):
    blockSize_w = int(WINDOW_WIDTH / initial_state.board_width)
    blockSize_h = int(WINDOW_HEIGHT / initial_state.board_height)
    # Find the vehicle to move
    for index,vehicle in enumerate(initial_state.vehicles):
        if vehicle["id"] == vehicle_id:
            target_vehicle = vehicle
            target_index = index
            break

    if target_vehicle is not None:
        x, y= target_vehicle["x"], target_vehicle["y"]
    

        if target_vehicle["orientation"] == 'H':
            if "L" == move and x - 1 >= 0:
                pygame.draw.rect(screen, "gray", pygame.Rect( (x+target_vehicle["length"]-1) * blockSize_w, y*blockSize_h, blockSize_w, blockSize_h))
                initial_state.board[y][x+target_vehicle["length"]-1] = ' '
                x -= 1
                initial_state.board[y][x+target_vehicle["length"]-1] = target_vehicle["id"]
                
                initial_state.vehicles[target_index] = {
                    "id": target_vehicle["id"],
                    "x": x,
                    "y": y,
                    "length": target_vehicle["length"],
                    "orientation": target_vehicle["orientation"],
                    "color": target_vehicle["color"]
                }

            elif "R" == move and x + target_vehicle["length"] < initial_state.board_width:
                pygame.draw.rect(screen, "gray", pygame.Rect(x* blockSize_w, y*blockSize_h, blockSize_w, blockSize_h))
                initial_state.board[y][x + target_vehicle["length"]] = ' '
                x += target_vehicle["length"]
                initial_state.board[y][x] = target_vehicle["id"]

                initial_state.vehicles[target_index] = {
                    "id": target_vehicle["id"],
                    "x": x-target_vehicle["length"]+1,
                    "y": y,
                    "length": target_vehicle["length"],
                    "orientation": target_vehicle["orientation"],
                    "color": target_vehicle["color"]
                }

        else:
            if "U" == move and y-1 >= 0:
                pygame.draw.rect(screen, "gray", pygame.Rect(x*blockSize_w, (y+target_vehicle["length"]-1)*blockSize_h, blockSize_w, blockSize_h))
                initial_state.board[y+target_vehicle["length"]-1][x] = ' '
                y -= 1  
                initial_state.board[y][x] = target_vehicle["id"]


                initial_state.vehicles[target_index] = {
                    "id": target_vehicle["id"],
                    "x": x,
                    "y": y,
                    "length": target_vehicle["length"],
                    "orientation": target_vehicle["orientation"],
                    "color": target_vehicle["color"]
                }

            elif "D" == move and y + target_vehicle["length"] - 1 <= initial_state.board_height:
                pygame.draw.rect(screen, "gray", pygame.Rect( x*blockSize_w, y*blockSize_h, blockSize_w, blockSize_h))
                initial_state.board[y][x] = ' '
                y += target_vehicle["length"]
                initial_state.board[y][x] = target_vehicle["id"]

                initial_state.vehicles[target_index] = {
                    "id": target_vehicle["id"],
                    "x": x,
                    "y": y-target_vehicle["length"]+1,
                    "length": target_vehicle["length"],
                    "orientation": target_vehicle["orientation"],
                    "color": target_vehicle["color"]
                }


        car_rect = pygame.Rect(
            x * blockSize_w,
            y * blockSize_h,
            blockSize_w if target_vehicle["orientation"] == 'H' else blockSize_w,
            blockSize_h if target_vehicle["orientation"] == 'V' else blockSize_h
        )

    
        pygame.draw.rect(screen, target_vehicle["color"], car_rect)


def main():
    global screen, clock,initial_state

    initial_state = RushHourPuzzle('2-b.csv')
    RushHourPuzzle.printRushHourBoard(initial_state.board)
    goal_node, step = Search.Astar(initial_state)

    if goal_node is None:
        print("No solution")
        exit(0)


    
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("gray")

        drawGrid(initial_state)
        sleep(2)
        solution = goal_node.getSolution()
        print(len(solution))
        print(solution)

        solution.remove('')
     
        for i,s in enumerate(solution):
            print(f"next move : {s}")
            vehicle_id, move_direction = s.split(':')
            pygame.display.set_caption(f"Next step : {s} , number of steps : {len(solution)}")
          
            make_move(initial_state, vehicle_id, move_direction)
            pygame.display.flip()
            clock.tick(60)
            sleep(0.3)
        
            if i == len(solution)-1:
                running=False

        pygame.quit()



if __name__ == "__main__":
    main()



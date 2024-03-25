from Population import Population
import pygame
import sys

WIDTH, HEIGHT = 600, 600
PADDING = 60
BLOCK_SIZE = (WIDTH)// 10
FPS = 40
GREEN = (239,238,211)
DARKGREEN = (119,150,84)
BLACK = (0, 0, 0)

horse_image = pygame.image.load('knight.png')
horse_image = pygame.transform.scale(horse_image, (BLOCK_SIZE, BLOCK_SIZE))


def draw_text_with_background(text, position, font, screen, text_color, background_color):
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect()
    background_rect = pygame.Rect(position, (text_rect.width, text_rect.height))
    pygame.draw.rect(screen, background_color, background_rect)
    screen.blit(text_surface, position)


def draw_board(path, screen):
    screen.fill(GREEN)

    number_font = pygame.font.Font(None, 36)
    

    for row in range(8):
        draw_text_with_background(str(row + 1), (PADDING // 2, PADDING + 20 + row * PADDING), number_font, screen, BLACK, GREEN)
        draw_text_with_background(str(row + 1), (PADDING * row + PADDING + 20, BLOCK_SIZE - PADDING // 2), number_font, screen, BLACK, GREEN)
        draw_text_with_background(str(row + 1), (WIDTH - PADDING // 2 - 20, PADDING + 20 + row * PADDING), number_font, screen, BLACK, GREEN)


    for col in range(8):
        draw_text_with_background(str(col + 1), (PADDING * col + PADDING + 20, PADDING // 2), number_font, screen, BLACK, GREEN)
        draw_text_with_background(str(col + 1), (PADDING * col + PADDING + 20, BLOCK_SIZE - PADDING // 2), number_font, screen, BLACK, GREEN)

        draw_text_with_background(str(col + 1), (PADDING * col + PADDING + 20, HEIGHT - PADDING // 2 - 20), number_font, screen, BLACK, GREEN)

    for row in range(8):
        for col in range(8):
            color = GREEN if (row + col) % 2 == 0 else DARKGREEN
            pygame.draw.rect(screen, color, (col * BLOCK_SIZE + PADDING, row * BLOCK_SIZE + PADDING, BLOCK_SIZE, BLOCK_SIZE))



    previous = path[0]

    for i, (x, y) in enumerate(path):
        color = GREEN if (x+y) % 2 != 0 else DARKGREEN
        pygame.draw.rect(screen, color, (previous[1] * BLOCK_SIZE + PADDING,previous[0] * BLOCK_SIZE + PADDING, BLOCK_SIZE, BLOCK_SIZE))
        green_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
        green_surface.fill((0, 255, 0, 110)) 
        screen.blit(green_surface, (previous[1] * BLOCK_SIZE + PADDING, previous[0] * BLOCK_SIZE + PADDING))
        index_text = number_font.render(str(i), True, BLACK)
        screen.blit(index_text, (previous[1] * BLOCK_SIZE + PADDING + 20, PADDING + 20 + previous[0] * PADDING, BLOCK_SIZE, BLOCK_SIZE))
        pygame.display.flip()
        screen.blit(horse_image, (y * BLOCK_SIZE + PADDING, x * BLOCK_SIZE + PADDING))
        pygame.display.flip()
        pygame.time.delay(300)
        previous = (x,y)

    color = GREEN if (row + col) % 2 != 0 else DARKGREEN
    pygame.draw.rect(screen, color, (previous[1] * BLOCK_SIZE + PADDING,previous[0] * BLOCK_SIZE + PADDING, BLOCK_SIZE, BLOCK_SIZE))
    green_surface = pygame.Surface((BLOCK_SIZE, BLOCK_SIZE), pygame.SRCALPHA)
    green_surface.fill((0, 255, 0, 110))
    screen.blit(green_surface, (previous[1] * BLOCK_SIZE + PADDING, previous[0] * BLOCK_SIZE + PADDING))
    index_text = number_font.render(str(i+1), True, BLACK)
    screen.blit(index_text, (previous[1] * BLOCK_SIZE + PADDING + 20, PADDING + 20 + previous[0] * PADDING, BLOCK_SIZE, BLOCK_SIZE))
    pygame.display.flip()
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()




def display_board_CLI(path):
    board = [[' ' for _ in range(8)] for _ in range(8)]

    for i, (x, y) in enumerate(path):
        board[x][y] = str(i + 1)

    print("+" + "-" * 30 + "+")
    for row in board:
        print("|", end=" ")
        for cell in row:
            print(cell.center(2), end=" | ")
        print("\n+" + "-" * 30 + "+")




def main():

    population_size = 50
    population = Population(population_size)
    while True:
        population.check_population()
        max_fit,best_solution = population.evaluate()
        if max_fit == 64:
            break
        population.create_new_generation()

    print(f"Solved with {population.generation} generations\n The path is {best_solution.path}\n")

    pygame.init()
    global screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    pygame.display.set_caption("Amine Boucenna knight's Tour")
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_board(best_solution.path,screen)
        
        clock.tick(FPS)


if __name__ == "__main__":
    main()

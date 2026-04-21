import pygame                                # game library
import random                                # used to pick random food positions

pygame.init()                                # start pygame modules

CELL = 20                                    # size of one grid cell in pixels
COLS = 30                                    # number of grid columns
ROWS = 25                                    # number of grid rows
WIDTH = COLS * CELL                          # total window width in pixels
TOP_BAR = 40                                 # height of the top bar (score and level)
HEIGHT = ROWS * CELL + TOP_BAR               # total window height including the top bar

screen = pygame.display.set_mode((WIDTH, HEIGHT))   # open the game window
pygame.display.set_caption("Snake")          # window title

# colors (R, G, B)
BG = (20, 20, 30)                            # dark background color
SNAKE_HEAD = (70, 200, 70)                   # brighter green for the snake's head
SNAKE_BODY = (50, 160, 50)                   # darker green for the body
FOOD = (220, 60, 60)                         # red food color
WHITE = (240, 240, 240)                      # text color
WALL = (100, 100, 110)                       # color of the top info bar

clock = pygame.time.Clock()                  # controls game speed (FPS)
font = pygame.font.SysFont("Arial", 22, bold=True)      # regular font
big_font = pygame.font.SysFont("Arial", 48, bold=True)  # bigger font for the game-over message


def random_food(snake):
    # keep picking random cells until we find one that is not on the snake
    while True:
        x = random.randint(0, COLS - 1)      # random column inside the grid
        y = random.randint(0, ROWS - 1)      # random row inside the grid
        if (x, y) not in snake:              # skip if this cell is on the snake's body
            return (x, y)                    # return the empty cell


def draw_cell(cell, color):
    # draw one grid cell at its pixel position
    x, y = cell
    rect = pygame.Rect(x * CELL, TOP_BAR + y * CELL, CELL, CELL)   # pixel position; y shifted by the top bar
    pygame.draw.rect(screen, color, rect)                          # filled color
    pygame.draw.rect(screen, BG, rect, 1)                          # thin border so cells look separated


def draw_bar(score, level):
    pygame.draw.rect(screen, WALL, (0, 0, WIDTH, TOP_BAR))         # top bar background
    score_text = font.render(f"Score: {score}", True, WHITE)       # score text
    level_text = font.render(f"Level: {level}", True, WHITE)       # level text
    screen.blit(score_text, (10, 8))                               # draw score on the left
    screen.blit(level_text, (WIDTH - 120, 8))                      # draw level on the right


def reset_game():
    # place a 3-cell snake in the middle, moving to the right
    start_x = COLS // 2
    start_y = ROWS // 2
    snake = [(start_x - 2, start_y), (start_x - 1, start_y), (start_x, start_y)]
    direction = (1, 0)                       # (dx, dy) — currently moving right
    food = random_food(snake)                # first food position
    score = 0                                # reset score
    level = 1                                # start at level 1
    speed = 8                                # FPS at level 1 (slow)
    return snake, direction, food, score, level, speed


# build the initial state
snake, direction, food, score, level, speed = reset_game()
game_over = False                            # becomes True when the snake dies

FOODS_PER_LEVEL = 3                          # level up after this many foods

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:        # user closed the window
            running = False
        elif event.type == pygame.KEYDOWN:   # a key was pressed
            # R restarts the game only after game over
            if game_over and event.key == pygame.K_r:
                snake, direction, food, score, level, speed = reset_game()
                game_over = False
            # change direction, but block reversing directly (would kill the snake)
            if not game_over:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)      # up
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)       # down
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)      # left
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)       # right

    if not game_over:
        head_x, head_y = snake[-1]                                  # current head position
        new_head = (head_x + direction[0], head_y + direction[1])   # where the head moves next

        # wall collision: new head is outside the grid
        if (new_head[0] < 0 or new_head[0] >= COLS or
                new_head[1] < 0 or new_head[1] >= ROWS):
            game_over = True

        # self collision: new head hits the body
        elif new_head in snake:
            game_over = True

        else:
            snake.append(new_head)                       # move forward: add the new head
            if new_head == food:
                score += 1                               # count the food
                food = random_food(snake)                # spawn a new food somewhere safe
                # every few foods → level up and go faster
                if score % FOODS_PER_LEVEL == 0:
                    level += 1                           # go up one level
                    speed += 2                           # add 2 FPS so it feels faster
                # NOTE: we didn't pop the tail → the snake grew by one cell
            else:
                snake.pop(0)                             # no food → drop the tail so length stays the same

    screen.fill(BG)                          # clear the screen
    draw_bar(score, level)                   # draw the top info bar
    draw_cell(food, FOOD)                    # draw the food
    # draw the body (every cell except the last one, which is the head)
    for cell in snake[:-1]:
        draw_cell(cell, SNAKE_BODY)
    # draw the head with a brighter color on top of the body
    draw_cell(snake[-1], SNAKE_HEAD)

    if game_over:
        msg = big_font.render("GAME OVER", True, WHITE)             # large title
        tip = font.render("Press R to restart", True, WHITE)         # small hint
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        screen.blit(tip, tip.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

    pygame.display.flip()                    # show the drawn frame
    clock.tick(speed)                        # speed grows each level, so the snake moves faster

pygame.quit()                                # close pygame at the end

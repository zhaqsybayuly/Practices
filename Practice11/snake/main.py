import pygame                                # game library
import random                                # for random food positions / weights

pygame.init()                                # start pygame

CELL = 20
COLS = 30
ROWS = 25
WIDTH = COLS * CELL
TOP_BAR = 40
HEIGHT = ROWS * CELL + TOP_BAR

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# colors
BG = (20, 20, 30)
SNAKE_HEAD = (70, 200, 70)
SNAKE_BODY = (50, 160, 50)
WHITE = (240, 240, 240)
WALL = (100, 100, 110)

# food types: weight (points) → color
FOOD_TYPES = {
    1: (220, 60, 60),       # red — 1 point, common
    2: (240, 180, 50),      # yellow — 2 points
    3: (90, 200, 230),      # cyan — 3 points, rare
}

# how long each food stays on the board before disappearing (seconds)
FOOD_LIFETIME = 5.0

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22, bold=True)
big_font = pygame.font.SysFont("Arial", 48, bold=True)


def random_food(snake):
    # pick a random empty cell + random weight (rare items show up less often)
    while True:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) not in snake:
            weight = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
            return {"pos": (x, y), "weight": weight, "spawn_time": pygame.time.get_ticks()}


def draw_cell(cell, color):
    x, y = cell
    rect = pygame.Rect(x * CELL, TOP_BAR + y * CELL, CELL, CELL)
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BG, rect, 1)


def draw_food(food):
    color = FOOD_TYPES[food["weight"]]
    draw_cell(food["pos"], color)
    # show the weight number inside the food cell
    x, y = food["pos"]
    label = pygame.font.SysFont("Arial", 14, bold=True).render(str(food["weight"]), True, BG)
    screen.blit(label, label.get_rect(center=(x * CELL + CELL // 2, TOP_BAR + y * CELL + CELL // 2)))


def draw_bar(score, level, time_left):
    pygame.draw.rect(screen, WALL, (0, 0, WIDTH, TOP_BAR))
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    timer_text = font.render(f"Food: {time_left:.1f}s", True, WHITE)
    screen.blit(score_text, (10, 8))
    screen.blit(timer_text, (WIDTH // 2 - 60, 8))
    screen.blit(level_text, (WIDTH - 110, 8))


def reset_game():
    start_x = COLS // 2
    start_y = ROWS // 2
    snake = [(start_x - 2, start_y), (start_x - 1, start_y), (start_x, start_y)]
    direction = (1, 0)
    food = random_food(snake)
    score = 0
    level = 1
    speed = 8
    foods_eaten = 0
    return snake, direction, food, score, level, speed, foods_eaten


snake, direction, food, score, level, speed, foods_eaten = reset_game()
game_over = False
FOODS_PER_LEVEL = 3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_r:
                snake, direction, food, score, level, speed, foods_eaten = reset_game()
                game_over = False
            if not game_over:
                if event.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

    if not game_over:
        head_x, head_y = snake[-1]
        new_head = (head_x + direction[0], head_y + direction[1])

        # wall collision
        if (new_head[0] < 0 or new_head[0] >= COLS or
                new_head[1] < 0 or new_head[1] >= ROWS):
            game_over = True
        # self collision
        elif new_head in snake:
            game_over = True
        else:
            snake.append(new_head)
            if new_head == food["pos"]:
                # add weight as score points
                score += food["weight"]
                foods_eaten += 1
                food = random_food(snake)
                # level up every FOODS_PER_LEVEL items eaten
                if foods_eaten % FOODS_PER_LEVEL == 0:
                    level += 1
                    speed += 2
            else:
                snake.pop(0)

        # check if the food expired (timer ran out → respawn)
        elapsed_ms = pygame.time.get_ticks() - food["spawn_time"]
        if elapsed_ms / 1000 > FOOD_LIFETIME:
            food = random_food(snake)

    # how much time the current food has left
    time_left = max(0, FOOD_LIFETIME - (pygame.time.get_ticks() - food["spawn_time"]) / 1000)

    screen.fill(BG)
    draw_bar(score, level, time_left)
    draw_food(food)
    for cell in snake[:-1]:
        draw_cell(cell, SNAKE_BODY)
    draw_cell(snake[-1], SNAKE_HEAD)

    if game_over:
        msg = big_font.render("GAME OVER", True, WHITE)
        tip = font.render("Press R to restart", True, WHITE)
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
        screen.blit(tip, tip.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()

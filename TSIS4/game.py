import pygame
import random
import json
from db import save_session, personal_best

CELL = 20
COLS = 30
ROWS = 25
WIDTH = COLS * CELL
TOP_BAR = 40
HEIGHT = ROWS * CELL + TOP_BAR

BG = (20, 20, 30)
WHITE = (240, 240, 240)
WALL = (100, 100, 110)
OBSTACLE = (160, 160, 170)
POISON = (130, 30, 30)

# food types: weight → color (Practice 11)
FOOD_TYPES = {1: (220, 60, 60), 2: (240, 180, 50), 3: (90, 200, 230)}
FOOD_LIFETIME = 5.0

# power-ups: type → color
POWERUPS = {
    "boost":  (255, 140, 0),
    "slow":   (100, 200, 255),
    "shield": (240, 200, 40),
}
POWERUP_LIFETIME = 8.0


def load_settings():
    with open("settings.json") as f:
        return json.load(f)


def random_empty_cell(snake, food, obstacles, powerup=None):
    while True:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) in snake:
            continue
        if food and (x, y) == food.get("pos"):
            continue
        if (x, y) in obstacles:
            continue
        if powerup and (x, y) == powerup.get("pos"):
            continue
        return (x, y)


def random_food(snake, obstacles, powerup=None, poison=False):
    pos = random_empty_cell(snake, None, obstacles, powerup)
    if poison:
        return {"pos": pos, "weight": -2, "spawn_time": pygame.time.get_ticks(), "poison": True}
    weight = random.choices([1, 2, 3], weights=[60, 30, 10])[0]
    return {"pos": pos, "weight": weight, "spawn_time": pygame.time.get_ticks(), "poison": False}


def random_powerup(snake, food, obstacles):
    pos = random_empty_cell(snake, food, obstacles)
    return {"pos": pos, "type": random.choice(list(POWERUPS)),
            "spawn_time": pygame.time.get_ticks()}


def random_obstacles(level, snake):
    """Add a small set of obstacles for a given level (called at level transitions)."""
    obstacles = set()
    n = (level - 2) * 2 if level >= 3 else 0
    while len(obstacles) < n:
        x = random.randint(0, COLS - 1)
        y = random.randint(0, ROWS - 1)
        if (x, y) in snake:
            continue
        obstacles.add((x, y))
    return obstacles


def run_game(player_id, username):
    settings = load_settings()
    snake_color = tuple(settings["snake_color"])
    show_grid = settings["grid"]

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake — TSIS4")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18, bold=True)
    big_font = pygame.font.SysFont("Arial", 48, bold=True)

    snake = [(COLS // 2 - 2, ROWS // 2), (COLS // 2 - 1, ROWS // 2), (COLS // 2, ROWS // 2)]
    direction = (1, 0)
    obstacles = set()
    food = random_food(snake, obstacles)
    poison = None
    powerup = None
    score = 0
    level = 1
    speed = 8
    foods_eaten = 0
    pb = personal_best(player_id)

    has_shield = False
    boost_until = 0
    slow_until = 0

    running = True
    game_over = False

    while running and not game_over:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_UP and direction != (0, 1):
                    direction = (0, -1)
                elif ev.key == pygame.K_DOWN and direction != (0, -1):
                    direction = (0, 1)
                elif ev.key == pygame.K_LEFT and direction != (1, 0):
                    direction = (-1, 0)
                elif ev.key == pygame.K_RIGHT and direction != (-1, 0):
                    direction = (1, 0)

        # move snake
        head = snake[-1]
        new_head = (head[0] + direction[0], head[1] + direction[1])

        # wall collision
        if not (0 <= new_head[0] < COLS and 0 <= new_head[1] < ROWS):
            if has_shield:
                has_shield = False
                # don't actually move into the wall — keep head where it was
                pass
            else:
                game_over = True
                break

        # self collision
        if new_head in snake:
            if has_shield:
                has_shield = False
            else:
                game_over = True
                break

        # obstacle collision
        if new_head in obstacles:
            if has_shield:
                has_shield = False
            else:
                game_over = True
                break

        snake.append(new_head)
        ate_food = False

        if food and new_head == food["pos"]:
            score += food["weight"]
            foods_eaten += 1
            ate_food = True
            food = random_food(snake, obstacles, powerup)
            if foods_eaten % 3 == 0:
                level += 1
                speed += 2
                if level >= 3:
                    obstacles = random_obstacles(level, snake)

        if poison and new_head == poison["pos"]:
            # poison: shorten snake by 2
            for _ in range(2):
                if len(snake) > 1:
                    snake.pop(0)
            if len(snake) <= 1:
                game_over = True
                break
            poison = None

        if powerup and new_head == powerup["pos"]:
            t = powerup["type"]
            now = pygame.time.get_ticks()
            if t == "boost":
                boost_until = now + 5000
            elif t == "slow":
                slow_until = now + 5000
            elif t == "shield":
                has_shield = True
            powerup = None

        if not ate_food:
            snake.pop(0)

        # food expires
        if food and (pygame.time.get_ticks() - food["spawn_time"]) / 1000 > FOOD_LIFETIME:
            food = random_food(snake, obstacles, powerup)

        # poison spawns randomly every ~7 seconds
        if not poison and random.random() < 0.005:
            poison = {"pos": random_empty_cell(snake, food, obstacles, powerup),
                      "spawn_time": pygame.time.get_ticks(), "poison": True}
        if poison and (pygame.time.get_ticks() - poison["spawn_time"]) / 1000 > FOOD_LIFETIME * 1.5:
            poison = None

        # powerup spawns randomly
        if not powerup and random.random() < 0.003:
            powerup = random_powerup(snake, food, obstacles)
        if powerup and (pygame.time.get_ticks() - powerup["spawn_time"]) / 1000 > POWERUP_LIFETIME:
            powerup = None

        # current movement speed
        now = pygame.time.get_ticks()
        cur_speed = speed
        if now < boost_until:
            cur_speed += 4
        if now < slow_until:
            cur_speed = max(3, cur_speed - 4)

        # ---- draw ----
        screen.fill(BG)
        # top bar
        pygame.draw.rect(screen, WALL, (0, 0, WIDTH, TOP_BAR))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Level: {level}", True, WHITE), (160, 10))
        screen.blit(font.render(f"Best: {pb}", True, WHITE), (300, 10))
        if has_shield:
            screen.blit(font.render("SHIELD", True, (240, 200, 40)), (450, 10))

        # grid overlay (settings)
        if show_grid:
            for x in range(COLS):
                for y in range(ROWS):
                    pygame.draw.rect(screen, (35, 35, 50),
                                     (x * CELL, TOP_BAR + y * CELL, CELL, CELL), 1)

        # obstacles
        for (x, y) in obstacles:
            pygame.draw.rect(screen, OBSTACLE, (x * CELL, TOP_BAR + y * CELL, CELL, CELL))

        # food
        if food:
            x, y = food["pos"]
            pygame.draw.rect(screen, FOOD_TYPES[food["weight"]],
                             (x * CELL, TOP_BAR + y * CELL, CELL, CELL))

        # poison
        if poison:
            x, y = poison["pos"]
            pygame.draw.rect(screen, POISON, (x * CELL, TOP_BAR + y * CELL, CELL, CELL))

        # powerup
        if powerup:
            x, y = powerup["pos"]
            pygame.draw.rect(screen, POWERUPS[powerup["type"]],
                             (x * CELL, TOP_BAR + y * CELL, CELL, CELL))
            screen.blit(font.render(powerup["type"][0].upper(), True, BG),
                        (x * CELL + 5, TOP_BAR + y * CELL))

        # snake
        for (x, y) in snake:
            pygame.draw.rect(screen, snake_color, (x * CELL, TOP_BAR + y * CELL, CELL, CELL))

        pygame.display.flip()
        clock.tick(cur_speed)

    # save the session to the database
    save_session(player_id, score, level)
    return score, level

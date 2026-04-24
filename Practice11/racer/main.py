import pygame                                # game library for graphics and input
import random                                # for random positions and coin types

pygame.init()                                # start pygame

WIDTH = 500
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")

# colors
GRAY = (80, 80, 80)
WHITE = (255, 255, 255)
GREEN = (30, 150, 30)
RED = (220, 30, 30)
BLACK = (0, 0, 0)

# coin colors per weight (bronze, silver, gold)
COIN_COLORS = {
    1: (200, 130, 60),       # bronze — 1 point
    3: (200, 200, 200),      # silver — 3 points
    5: (240, 200, 40),       # gold   — 5 points
}

clock = pygame.time.Clock()
FPS = 60
font = pygame.font.SysFont("Arial", 24, bold=True)

# player
CAR_W, CAR_H = 50, 80
player_x = WIDTH // 2 - CAR_W // 2
player_y = HEIGHT - CAR_H - 20
player_speed = 5

# load car images
player_img = pygame.image.load("img/red_car.png").convert_alpha()
player_img = pygame.transform.smoothscale(player_img, (CAR_W, CAR_H))
enemy_img = pygame.image.load("img/blue_car.png").convert_alpha()
enemy_img = pygame.transform.smoothscale(enemy_img, (CAR_W, CAR_H))
enemy_img = pygame.transform.rotate(enemy_img, 180)   # face the player

# enemy
enemy_w, enemy_h = 50, 80
enemy_x = random.randint(60, WIDTH - 60 - enemy_w)
enemy_y = -enemy_h
enemy_speed = 5

# coin — now has a "weight" that decides color and points
coin_r = 12
def new_coin():
    # pick a random weight: bronze (most common), silver, gold (rarest)
    weight = random.choices([1, 3, 5], weights=[60, 30, 10])[0]
    x = random.randint(60, WIDTH - 60)
    y = -random.randint(100, 400)
    return {"x": x, "y": y, "weight": weight}

coin = new_coin()
coin_speed = 4

coins_collected = 0     # total points (sum of coin weights)
lane_offset = 0

# every COIN_THRESHOLD points → enemy moves faster
COIN_THRESHOLD = 10


def draw_road():
    screen.fill(GREEN)
    pygame.draw.rect(screen, GRAY, (50, 0, WIDTH - 100, HEIGHT))
    for y in range(-40, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 3, y + lane_offset, 6, 20))


def draw_player():
    screen.blit(player_img, (player_x, player_y))


def draw_enemy():
    screen.blit(enemy_img, (enemy_x, enemy_y))


def draw_coin():
    color = COIN_COLORS[coin["weight"]]
    pygame.draw.circle(screen, color, (coin["x"], coin["y"]), coin_r)
    pygame.draw.circle(screen, BLACK, (coin["x"], coin["y"]), coin_r, 2)
    # show the weight inside the coin
    label = pygame.font.SysFont("Arial", 14, bold=True).render(str(coin["weight"]), True, BLACK)
    screen.blit(label, label.get_rect(center=(coin["x"], coin["y"])))


def draw_score():
    text = font.render(f"Coins: {coins_collected}", True, WHITE)
    rect = text.get_rect(topright=(WIDTH - 10, 10))
    screen.blit(text, rect)


def rects_overlap(ax, ay, aw, ah, bx, by, bw, bh):
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x + CAR_W < WIDTH - 50:
            player_x += player_speed

        # enemy moves down with current speed (faster as coins grow)
        enemy_y += enemy_speed
        if enemy_y > HEIGHT:
            enemy_y = -enemy_h
            enemy_x = random.randint(60, WIDTH - 60 - enemy_w)

        # move coin
        coin["y"] += coin_speed
        if coin["y"] - coin_r > HEIGHT:
            coin = new_coin()

        lane_offset += 6
        if lane_offset >= 40:
            lane_offset = 0

        # collision with enemy → game over
        if rects_overlap(player_x, player_y, CAR_W, CAR_H,
                         enemy_x, enemy_y, enemy_w, enemy_h):
            game_over = True

        # collision with coin → add points based on weight
        if rects_overlap(player_x, player_y, CAR_W, CAR_H,
                         coin["x"] - coin_r, coin["y"] - coin_r, coin_r * 2, coin_r * 2):
            coins_collected += coin["weight"]
            # speed up the enemy every COIN_THRESHOLD points
            new_level = coins_collected // COIN_THRESHOLD
            enemy_speed = 5 + new_level     # base 5 plus 1 per threshold
            coin = new_coin()

    draw_road()
    draw_coin()
    draw_enemy()
    draw_player()
    draw_score()

    if game_over:
        msg = font.render("GAME OVER - press R to restart", True, WHITE)
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_over = False
            coins_collected = 0
            enemy_speed = 5
            player_x = WIDTH // 2 - CAR_W // 2
            enemy_y = -enemy_h

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

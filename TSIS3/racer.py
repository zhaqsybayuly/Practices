import pygame
import random
import os
from persistence import add_score, load_settings

pygame.init()
WIDTH, HEIGHT = 500, 600

# colors
GRAY = (80, 80, 80)
WHITE = (255, 255, 255)
GREEN = (30, 150, 30)
BLACK = (0, 0, 0)
RED = (220, 30, 30)
YELLOW = (240, 200, 40)
BLUE = (30, 100, 220)
ORANGE = (255, 140, 0)

CAR_COLORS = {"red": RED, "blue": BLUE, "yellow": YELLOW}

# coin weights (Practice 11)
COIN_COLORS = {1: (200, 130, 60), 3: (200, 200, 200), 5: (240, 200, 40)}

# obstacles: oil spills slow the car briefly
# power-ups: nitro (speed), shield (block 1 hit), repair (clear obstacles)
POWERUPS = ["nitro", "shield", "repair"]


def run_game(player_name):
    """Main racer game loop. Returns (score, distance, coins) on game over."""
    settings = load_settings()
    car_color = CAR_COLORS.get(settings["car_color"], RED)
    difficulty_speed = {"easy": 4, "normal": 5, "hard": 7}[settings["difficulty"]]

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racer — TSIS3")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18, bold=True)

    CAR_W, CAR_H = 50, 80
    px = WIDTH // 2 - CAR_W // 2
    py = HEIGHT - CAR_H - 20

    enemy = {"x": random.randint(60, WIDTH - 110), "y": -CAR_H, "speed": difficulty_speed}
    coin = {"x": random.randint(60, WIDTH - 60), "y": -200, "weight": 1, "speed": 4}
    coin["weight"] = random.choices([1, 3, 5], weights=[60, 30, 10])[0]

    obstacle = {"x": random.randint(60, WIDTH - 100), "y": -800, "speed": 4}     # oil spill
    powerup = {"x": random.randint(60, WIDTH - 60), "y": -1200, "type": random.choice(POWERUPS), "speed": 4, "expire": None}

    coins_collected = 0
    distance = 0
    lane_offset = 0
    active_power = None        # currently active power-up
    power_expire = 0           # when active power expires (ms)
    has_shield = False
    boost_until = 0
    base_speed = difficulty_speed

    def reset_powerup():
        powerup["x"] = random.randint(60, WIDTH - 60)
        powerup["y"] = -random.randint(800, 1500)
        powerup["type"] = random.choice(POWERUPS)

    def reset_obstacle():
        obstacle["x"] = random.randint(60, WIDTH - 100)
        obstacle["y"] = -random.randint(400, 1000)

    def reset_coin():
        coin["x"] = random.randint(60, WIDTH - 60)
        coin["y"] = -random.randint(100, 400)
        coin["weight"] = random.choices([1, 3, 5], weights=[60, 30, 10])[0]

    def overlaps(ax, ay, aw, ah, bx, by, bw, bh):
        return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and px > 50:
            px -= 5
        if keys[pygame.K_RIGHT] and px + CAR_W < WIDTH - 50:
            px += 5

        # difficulty scaling: enemy speed grows with score
        enemy["speed"] = base_speed + coins_collected // 10
        if pygame.time.get_ticks() < boost_until:
            enemy["speed"] = max(1, enemy["speed"] - 3)   # nitro = relatively faster player

        enemy["y"] += enemy["speed"]
        if enemy["y"] > HEIGHT:
            enemy["y"] = -CAR_H
            enemy["x"] = random.randint(60, WIDTH - 110)

        coin["y"] += coin["speed"]
        if coin["y"] > HEIGHT + 20:
            reset_coin()

        obstacle["y"] += obstacle["speed"]
        if obstacle["y"] > HEIGHT + 40:
            reset_obstacle()

        powerup["y"] += powerup["speed"]
        if powerup["y"] > HEIGHT + 40:
            reset_powerup()

        lane_offset = (lane_offset + 6) % 40
        distance += 1

        # power-up timer expiry
        if active_power == "nitro" and pygame.time.get_ticks() > power_expire:
            active_power = None

        # collisions
        if overlaps(px, py, CAR_W, CAR_H, enemy["x"], enemy["y"], CAR_W, CAR_H):
            if has_shield:
                has_shield = False
                enemy["y"] = -CAR_H   # respawn enemy after blocked hit
                enemy["x"] = random.randint(60, WIDTH - 110)
            else:
                running = False

        if overlaps(px, py, CAR_W, CAR_H, obstacle["x"], obstacle["y"], 60, 30):
            # oil spill: lose 1 coin (small penalty), and bounce obstacle
            coins_collected = max(0, coins_collected - 1)
            reset_obstacle()

        if overlaps(px, py, CAR_W, CAR_H,
                    coin["x"] - 12, coin["y"] - 12, 24, 24):
            coins_collected += coin["weight"]
            reset_coin()

        if overlaps(px, py, CAR_W, CAR_H,
                    powerup["x"] - 14, powerup["y"] - 14, 28, 28):
            t = powerup["type"]
            if t == "nitro":
                active_power = "nitro"
                power_expire = pygame.time.get_ticks() + 4000
                boost_until = power_expire
            elif t == "shield":
                has_shield = True
                active_power = "shield"
            elif t == "repair":
                reset_obstacle()
                active_power = "repair"
            reset_powerup()

        # ---- draw ----
        screen.fill(GREEN)
        pygame.draw.rect(screen, GRAY, (50, 0, WIDTH - 100, HEIGHT))
        for y in range(-40, HEIGHT, 40):
            pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 3, y + lane_offset, 6, 20))

        # obstacle (oil spill)
        pygame.draw.ellipse(screen, BLACK, (obstacle["x"], obstacle["y"], 60, 30))

        # coin
        pygame.draw.circle(screen, COIN_COLORS[coin["weight"]], (coin["x"], coin["y"]), 12)
        pygame.draw.circle(screen, BLACK, (coin["x"], coin["y"]), 12, 2)

        # power-up box
        pcolor = {"nitro": ORANGE, "shield": (100, 200, 255), "repair": (100, 220, 100)}[powerup["type"]]
        pygame.draw.rect(screen, pcolor, (powerup["x"] - 14, powerup["y"] - 14, 28, 28))
        screen.blit(font.render(powerup["type"][0].upper(), True, BLACK),
                    (powerup["x"] - 6, powerup["y"] - 10))

        # enemy car
        pygame.draw.rect(screen, BLUE, (enemy["x"], enemy["y"], CAR_W, CAR_H), border_radius=6)

        # player car
        pygame.draw.rect(screen, car_color, (px, py, CAR_W, CAR_H), border_radius=6)
        if has_shield:
            pygame.draw.rect(screen, (100, 200, 255), (px - 4, py - 4, CAR_W + 8, CAR_H + 8), 3, border_radius=8)

        # HUD
        score = coins_collected * 10 + distance // 10
        screen.blit(font.render(f"Coins: {coins_collected}", True, WHITE), (10, 10))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 30))
        screen.blit(font.render(f"Distance: {distance}", True, WHITE), (10, 50))
        if active_power:
            ms_left = max(0, power_expire - pygame.time.get_ticks()) // 1000 if active_power == "nitro" else 0
            label = f"{active_power}" + (f" ({ms_left}s)" if active_power == "nitro" else "")
            screen.blit(font.render(label, True, ORANGE), (WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(60)

    final_score = coins_collected * 10 + distance // 10
    add_score(player_name, final_score, distance, coins_collected)
    return final_score, distance, coins_collected

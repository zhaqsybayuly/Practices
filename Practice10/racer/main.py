import pygame                                # game library for graphics and input
import random                                # used to pick random positions for enemy and coin

pygame.init()                                # start all pygame modules (required before using them)

WIDTH = 500                                  # window width in pixels
HEIGHT = 600                                 # window height in pixels
screen = pygame.display.set_mode((WIDTH, HEIGHT))   # create the game window
pygame.display.set_caption("Racer")          # set the title shown on the window

# colors in (Red, Green, Blue) format, each value from 0 to 255
GRAY = (80, 80, 80)                          # color of the road
WHITE = (255, 255, 255)                      # color of lane lines and text
GREEN = (30, 150, 30)                        # color of the grass on the sides
BLUE = (30, 100, 220)                        # color of the player car
RED = (220, 30, 30)                          # color of the enemy car
YELLOW = (240, 200, 40)                      # color of the coin
BLACK = (0, 0, 0)                            # color used for the car windows

clock = pygame.time.Clock()                  # controls how fast the game loop runs
FPS = 60                                     # target frames per second

font = pygame.font.SysFont("Arial", 24, bold=True)   # font for showing the coin counter

# player car settings
CAR_W, CAR_H = 50, 80                        # width and height of the player car
player_x = WIDTH // 2 - CAR_W // 2           # start the car centered horizontally
player_y = HEIGHT - CAR_H - 20               # place the car near the bottom of the screen
player_speed = 5                             # how many pixels the car moves per frame

# enemy car settings
enemy_w, enemy_h = 50, 80                    # size of the enemy car
enemy_x = random.randint(60, WIDTH - 60 - enemy_w)  # random x on the road (60 is the grass margin)
enemy_y = -enemy_h                           # start above the screen so it falls down
enemy_speed = 5                              # how fast the enemy moves down

# coin settings
coin_r = 12                                  # radius of the coin circle
coin_x = random.randint(60, WIDTH - 60)      # random x inside the road area
coin_y = -200                                # start above the screen
coin_speed = 4                               # how fast the coin falls

coins_collected = 0                          # counter for collected coins

lane_offset = 0                              # offset for the dashed lane line animation


def draw_road():
    screen.fill(GREEN)                                                # fill the background with grass color
    pygame.draw.rect(screen, GRAY, (50, 0, WIDTH - 100, HEIGHT))      # draw the gray road in the middle
    # draw dashed white lines on the road center, shifted by lane_offset each frame
    for y in range(-40, HEIGHT, 40):
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - 3, y + lane_offset, 6, 20))


def draw_player():
    # draw the player car body
    pygame.draw.rect(screen, BLUE, (player_x, player_y, CAR_W, CAR_H), border_radius=6)
    # draw a small black windshield on top of the car
    pygame.draw.rect(screen, BLACK, (player_x + 8, player_y + 12, CAR_W - 16, 20), border_radius=3)


def draw_enemy():
    # draw the enemy car body
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, enemy_w, enemy_h), border_radius=6)
    # draw a small windshield on the bottom of the enemy car (it's facing the player)
    pygame.draw.rect(screen, BLACK, (enemy_x + 8, enemy_y + enemy_h - 32, enemy_w - 16, 20), border_radius=3)


def draw_coin():
    pygame.draw.circle(screen, YELLOW, (coin_x, coin_y), coin_r)      # filled yellow circle
    pygame.draw.circle(screen, BLACK, (coin_x, coin_y), coin_r, 2)    # thin black outline


def draw_score():
    text = font.render(f"Coins: {coins_collected}", True, WHITE)      # render the counter text
    rect = text.get_rect(topright=(WIDTH - 10, 10))                   # place it in the top-right corner
    screen.blit(text, rect)                                           # draw it on the screen


def rects_overlap(ax, ay, aw, ah, bx, by, bw, bh):
    # two rectangles overlap only if they overlap on both x and y axis
    return ax < bx + bw and ax + aw > bx and ay < by + bh and ay + ah > by


running = True                                # main loop flag
game_over = False                             # becomes True when the player crashes

while running:
    # handle events like closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:         # user clicked the close button
            running = False

    if not game_over:
        keys = pygame.key.get_pressed()       # get the state of all keys right now
        # move left if the left arrow is held and there is still road to the left
        if keys[pygame.K_LEFT] and player_x > 50:
            player_x -= player_speed
        # move right if the right arrow is held and there is still road to the right
        if keys[pygame.K_RIGHT] and player_x + CAR_W < WIDTH - 50:
            player_x += player_speed

        enemy_y += enemy_speed                # move the enemy car down
        if enemy_y > HEIGHT:                  # enemy went past the bottom of the screen
            enemy_y = -enemy_h                # send it back above the screen
            enemy_x = random.randint(60, WIDTH - 60 - enemy_w)  # pick a new random x

        coin_y += coin_speed                  # move the coin down
        if coin_y - coin_r > HEIGHT:          # coin left the screen
            coin_y = -random.randint(100, 400)            # random y above the screen
            coin_x = random.randint(60, WIDTH - 60)       # random x on the road

        lane_offset += 6                      # shift the dashed lines down a little
        if lane_offset >= 40:                 # each dash is 40 px tall, so wrap after 40
            lane_offset = 0

        # check if the player collided with the enemy car → game over
        if rects_overlap(player_x, player_y, CAR_W, CAR_H,
                         enemy_x, enemy_y, enemy_w, enemy_h):
            game_over = True

        # check if the player touched the coin (we use a square around the circle for simplicity)
        if rects_overlap(player_x, player_y, CAR_W, CAR_H,
                         coin_x - coin_r, coin_y - coin_r, coin_r * 2, coin_r * 2):
            coins_collected += 1                         # add one coin to the counter
            coin_y = -random.randint(100, 400)           # reset coin above the screen
            coin_x = random.randint(60, WIDTH - 60)      # new random x

    # draw everything in order — background first, things on top after
    draw_road()
    draw_coin()
    draw_enemy()
    draw_player()
    draw_score()

    if game_over:
        msg = font.render("GAME OVER - press R to restart", True, WHITE)   # message text
        screen.blit(msg, msg.get_rect(center=(WIDTH // 2, HEIGHT // 2)))    # draw in the middle
        keys = pygame.key.get_pressed()       # check keys for restart
        if keys[pygame.K_r]:                  # R → restart
            game_over = False
            coins_collected = 0
            player_x = WIDTH // 2 - CAR_W // 2
            enemy_y = -enemy_h

    pygame.display.flip()                     # push the drawn frame to the screen
    clock.tick(FPS)                           # wait so we don't run faster than FPS

pygame.quit()                                 # clean up pygame when the loop ends

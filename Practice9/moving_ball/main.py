import pygame
from ball import Ball

pygame.init()

WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")
fps_clock = pygame.time.Clock()

ball = Ball(WIDTH, HEIGHT)

KEY_TO_DIR = {
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key in KEY_TO_DIR:
            ball.move(KEY_TO_DIR[event.key])

    screen.fill((255, 255, 255))
    ball.draw(screen)
    pygame.display.flip()
    fps_clock.tick(60)

pygame.quit()

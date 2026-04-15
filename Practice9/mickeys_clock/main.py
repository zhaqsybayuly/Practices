import pygame
from clock import MickeyClock

pygame.init()

WINDOW = 600
screen = pygame.display.set_mode((WINDOW, WINDOW))
pygame.display.set_caption("Mickey's Clock")
fps_clock = pygame.time.Clock()

mickey = MickeyClock(WINDOW)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    mickey.draw(screen)
    pygame.display.flip()
    fps_clock.tick(30)

pygame.quit()

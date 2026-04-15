import pygame
from player import Player

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont("Arial", 22)
fps_clock = pygame.time.Clock()

player = Player("music")


def draw_ui():
    screen.fill((30, 30, 40))

    if not player.has_tracks():
        msg = font.render("No music files found in 'music/' folder", True, (255, 255, 255))
        screen.blit(msg, (20, 130))
        pygame.display.flip()
        return

    lines = [
        f"Track: {player.current_name()}",
        f"Status: {player.status}",
        f"[{player.current + 1} / {len(player.tracks)}]",
        "",
        "P = Play   S = Stop",
        "N = Next   B = Back   Q = Quit",
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (20, 20 + i * 35))
    pygame.display.flip()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.back()
            elif event.key == pygame.K_q:
                running = False

    draw_ui()
    fps_clock.tick(30)

player.stop()
pygame.quit()

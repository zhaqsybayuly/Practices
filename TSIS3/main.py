import pygame
from persistence import load_leaderboard, load_settings, save_settings
from ui import button, text_input_screen
from racer import run_game

pygame.init()
WIDTH, HEIGHT = 500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer — TSIS3")
font = pygame.font.SysFont("Arial", 22, bold=True)
big_font = pygame.font.SysFont("Arial", 36, bold=True)
clock = pygame.time.Clock()


def main_menu():
    """Main menu with Play / Leaderboard / Settings / Quit."""
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = ev.pos
                if play_rect.collidepoint(pos):
                    name = text_input_screen(screen, font, "Enter your name:")
                    score, dist, coins = run_game(name)
                    game_over_screen(name, score, dist, coins)
                elif lb_rect.collidepoint(pos):
                    leaderboard_screen()
                elif set_rect.collidepoint(pos):
                    settings_screen()
                elif quit_rect.collidepoint(pos):
                    return

        screen.fill((30, 30, 40))
        title = big_font.render("RACER", True, (240, 200, 40))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        play_rect = pygame.Rect(WIDTH // 2 - 100, 200, 200, 50)
        lb_rect   = pygame.Rect(WIDTH // 2 - 100, 270, 200, 50)
        set_rect  = pygame.Rect(WIDTH // 2 - 100, 340, 200, 50)
        quit_rect = pygame.Rect(WIDTH // 2 - 100, 410, 200, 50)
        button(screen, play_rect, "Play",        font)
        button(screen, lb_rect,   "Leaderboard", font)
        button(screen, set_rect,  "Settings",    font)
        button(screen, quit_rect, "Quit",        font)
        pygame.display.flip()
        clock.tick(30)


def leaderboard_screen():
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and back.collidepoint(ev.pos):
                return

        screen.fill((30, 30, 40))
        title = big_font.render("Top 10", True, (240, 240, 240))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 50)))

        entries = load_leaderboard()
        for i, e in enumerate(entries[:10]):
            line = f"{i + 1}. {e['name']}  —  {e['score']} pts  ({e['distance']} dist, {e['coins']} coins)"
            screen.blit(font.render(line, True, (240, 240, 240)), (30, 110 + i * 30))

        back = pygame.Rect(WIDTH // 2 - 70, HEIGHT - 70, 140, 40)
        button(screen, back, "Back", font)
        pygame.display.flip()
        clock.tick(30)


def settings_screen():
    settings = load_settings()
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = ev.pos
                if sound_btn.collidepoint(pos):
                    settings["sound"] = not settings["sound"]
                elif color_btn.collidepoint(pos):
                    order = ["red", "blue", "yellow"]
                    settings["car_color"] = order[(order.index(settings["car_color"]) + 1) % len(order)]
                elif diff_btn.collidepoint(pos):
                    order = ["easy", "normal", "hard"]
                    settings["difficulty"] = order[(order.index(settings["difficulty"]) + 1) % len(order)]
                elif save_btn.collidepoint(pos):
                    save_settings(settings)
                    return

        screen.fill((30, 30, 40))
        title = big_font.render("Settings", True, (240, 240, 240))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 60)))

        sound_btn = pygame.Rect(WIDTH // 2 - 130, 150, 260, 50)
        color_btn = pygame.Rect(WIDTH // 2 - 130, 220, 260, 50)
        diff_btn  = pygame.Rect(WIDTH // 2 - 130, 290, 260, 50)
        save_btn  = pygame.Rect(WIDTH // 2 - 70, 400, 140, 50)

        button(screen, sound_btn, f"Sound: {'on' if settings['sound'] else 'off'}", font)
        button(screen, color_btn, f"Car: {settings['car_color']}", font)
        button(screen, diff_btn,  f"Difficulty: {settings['difficulty']}", font)
        button(screen, save_btn,  "Save & Back", font)

        pygame.display.flip()
        clock.tick(30)


def game_over_screen(name, score, distance, coins):
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if retry.collidepoint(ev.pos):
                    s, d, c = run_game(name)
                    return game_over_screen(name, s, d, c)
                if menu.collidepoint(ev.pos):
                    return

        screen.fill((30, 30, 40))
        title = big_font.render("GAME OVER", True, (220, 60, 60))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))
        screen.blit(font.render(f"{name}", True, (240, 240, 240)),
                    (WIDTH // 2 - 80, 180))
        screen.blit(font.render(f"Score: {score}", True, (240, 240, 240)),  (WIDTH // 2 - 80, 220))
        screen.blit(font.render(f"Distance: {distance}", True, (240, 240, 240)), (WIDTH // 2 - 80, 250))
        screen.blit(font.render(f"Coins: {coins}", True, (240, 240, 240)), (WIDTH // 2 - 80, 280))

        retry = pygame.Rect(WIDTH // 2 - 100, 380, 200, 50)
        menu  = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)
        button(screen, retry, "Retry",     font)
        button(screen, menu,  "Main Menu", font)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main_menu()
    pygame.quit()

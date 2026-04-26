import pygame
import json
from db import init_schema, get_or_create_player, top_10
from game import run_game, WIDTH, HEIGHT

pygame.init()
init_schema()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake — TSIS4")
font = pygame.font.SysFont("Arial", 22, bold=True)
big_font = pygame.font.SysFont("Arial", 36, bold=True)
clock = pygame.time.Clock()


def button(rect, label, active=False):
    bg = (180, 180, 250) if active else (210, 210, 215)
    pygame.draw.rect(screen, bg, rect, border_radius=6)
    pygame.draw.rect(screen, (60, 60, 60), rect, 2, border_radius=6)
    screen.blit(font.render(label, True, (20, 20, 20)),
                font.render(label, True, (20, 20, 20)).get_rect(center=rect.center))


def text_input(prompt):
    buf = ""
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_RETURN and buf.strip():
                    return buf.strip()
                elif ev.key == pygame.K_BACKSPACE:
                    buf = buf[:-1]
                elif ev.unicode and ev.unicode.isprintable():
                    buf += ev.unicode
        screen.fill((30, 30, 40))
        screen.blit(font.render(prompt, True, (240, 240, 240)),
                    (WIDTH // 2 - 150, 200))
        rect = pygame.Rect(WIDTH // 2 - 200, 260, 400, 50)
        pygame.draw.rect(screen, (240, 240, 240), rect)
        screen.blit(font.render(buf + "|", True, (20, 20, 20)),
                    (rect.x + 10, rect.y + 10))
        pygame.display.flip()
        clock.tick(30)


def main_menu():
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = ev.pos
                if play.collidepoint(pos):
                    name = text_input("Enter your username:")
                    pid = get_or_create_player(name)
                    score, level = run_game(pid, name)
                    game_over_screen(name, score, level)
                elif lb.collidepoint(pos):
                    leaderboard_screen()
                elif st.collidepoint(pos):
                    settings_screen()
                elif qt.collidepoint(pos):
                    return

        screen.fill((30, 30, 40))
        title = big_font.render("SNAKE", True, (70, 200, 70))
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        play = pygame.Rect(WIDTH // 2 - 100, 200, 200, 50)
        lb   = pygame.Rect(WIDTH // 2 - 100, 270, 200, 50)
        st   = pygame.Rect(WIDTH // 2 - 100, 340, 200, 50)
        qt   = pygame.Rect(WIDTH // 2 - 100, 410, 200, 50)
        button(play, "Play")
        button(lb,   "Leaderboard")
        button(st,   "Settings")
        button(qt,   "Quit")
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
        screen.blit(big_font.render("Top 10", True, (240, 240, 240)),
                    big_font.render("Top 10", True, (240, 240, 240)).get_rect(center=(WIDTH // 2, 50)))
        try:
            entries = top_10()
        except Exception:
            entries = []
        for i, e in enumerate(entries):
            uname, score, lvl, played = e
            line = f"{i + 1}. {uname}  —  {score} pts  L{lvl}  {played:%Y-%m-%d}"
            screen.blit(font.render(line, True, (240, 240, 240)), (30, 110 + i * 30))

        back = pygame.Rect(WIDTH // 2 - 70, HEIGHT - 70, 140, 40)
        button(back, "Back")
        pygame.display.flip()
        clock.tick(30)


def settings_screen():
    with open("settings.json") as f:
        settings = json.load(f)

    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = ev.pos
                if grid_btn.collidepoint(pos):
                    settings["grid"] = not settings["grid"]
                elif sound_btn.collidepoint(pos):
                    settings["sound"] = not settings["sound"]
                elif color_btn.collidepoint(pos):
                    palette = [[70, 200, 70], [220, 60, 60], [30, 100, 220], [240, 200, 40]]
                    cur = settings["snake_color"]
                    idx = next((i for i, c in enumerate(palette) if c == cur), 0)
                    settings["snake_color"] = palette[(idx + 1) % len(palette)]
                elif save_btn.collidepoint(pos):
                    with open("settings.json", "w") as f:
                        json.dump(settings, f, indent=2)
                    return

        screen.fill((30, 30, 40))
        screen.blit(big_font.render("Settings", True, (240, 240, 240)),
                    big_font.render("Settings", True, (240, 240, 240)).get_rect(center=(WIDTH // 2, 60)))

        grid_btn  = pygame.Rect(WIDTH // 2 - 130, 150, 260, 50)
        sound_btn = pygame.Rect(WIDTH // 2 - 130, 220, 260, 50)
        color_btn = pygame.Rect(WIDTH // 2 - 130, 290, 260, 50)
        save_btn  = pygame.Rect(WIDTH // 2 - 70, 400, 140, 50)

        button(grid_btn,  f"Grid: {'on' if settings['grid'] else 'off'}")
        button(sound_btn, f"Sound: {'on' if settings['sound'] else 'off'}")
        button(color_btn, f"Color: {settings['snake_color']}")
        button(save_btn,  "Save & Back")
        pygame.display.flip()
        clock.tick(30)


def game_over_screen(name, score, level):
    while True:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                exit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if retry.collidepoint(ev.pos):
                    from db import get_or_create_player
                    pid = get_or_create_player(name)
                    s, l = run_game(pid, name)
                    return game_over_screen(name, s, l)
                if menu.collidepoint(ev.pos):
                    return

        screen.fill((30, 30, 40))
        screen.blit(big_font.render("GAME OVER", True, (220, 60, 60)),
                    big_font.render("GAME OVER", True, (220, 60, 60)).get_rect(center=(WIDTH // 2, 100)))
        screen.blit(font.render(f"{name}", True, (240, 240, 240)), (WIDTH // 2 - 80, 180))
        screen.blit(font.render(f"Score: {score}", True, (240, 240, 240)), (WIDTH // 2 - 80, 220))
        screen.blit(font.render(f"Level: {level}", True, (240, 240, 240)), (WIDTH // 2 - 80, 250))

        retry = pygame.Rect(WIDTH // 2 - 100, 380, 200, 50)
        menu  = pygame.Rect(WIDTH // 2 - 100, 450, 200, 50)
        button(retry, "Retry")
        button(menu, "Main Menu")
        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    main_menu()
    pygame.quit()

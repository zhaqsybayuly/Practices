import pygame


def button(screen, rect, label, font, active=False):
    bg = (180, 180, 250) if active else (210, 210, 215)
    pygame.draw.rect(screen, bg, rect, border_radius=6)
    pygame.draw.rect(screen, (60, 60, 60), rect, 2, border_radius=6)
    text = font.render(label, True, (20, 20, 20))
    screen.blit(text, text.get_rect(center=rect.center))


def text_input_screen(screen, font, prompt):
    """Simple Pygame text-input screen. Returns the typed string when Enter is pressed."""
    buf = ""
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and buf.strip():
                    return buf.strip()
                elif event.key == pygame.K_BACKSPACE:
                    buf = buf[:-1]
                elif event.unicode and event.unicode.isprintable():
                    buf += event.unicode
        screen.fill((30, 30, 40))
        prompt_surf = font.render(prompt, True, (240, 240, 240))
        screen.blit(prompt_surf, prompt_surf.get_rect(center=(screen.get_width() // 2, 200)))
        rect = pygame.Rect(screen.get_width() // 2 - 200, 280, 400, 50)
        pygame.draw.rect(screen, (240, 240, 240), rect, border_radius=4)
        text = font.render(buf + "|", True, (20, 20, 20))
        screen.blit(text, (rect.x + 10, rect.y + 10))
        pygame.display.flip()
        clock.tick(30)

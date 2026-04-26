import pygame
import math
from datetime import datetime
from collections import deque

pygame.init()

WIDTH = 1100
HEIGHT = 650
TOOLBAR_H = 70

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint — TSIS2")

# canvas surface holds the drawings; toolbar drawn on top each frame
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("Arial", 13, bold=True)
big_font = pygame.font.SysFont("Arial", 18)
clock = pygame.time.Clock()

COLORS = [
    (0, 0, 0), (255, 255, 255),
    (220, 30, 30), (30, 150, 30), (30, 100, 220),
    (240, 200, 40), (200, 40, 200), (40, 200, 200), (255, 140, 0),
]

TOOLS = ["pencil", "line", "rect", "circle", "square",
         "right_tri", "equi_tri", "rhombus", "eraser", "fill", "text"]

# 3 brush size levels: small / medium / large
BRUSH_SIZES = {"S": 2, "M": 5, "L": 10}

current_color = COLORS[0]
current_tool = "pencil"
brush_label = "M"     # current size key

last_pos = None
shape_start = None
text_pos = None       # where the text cursor is placed
text_buffer = ""      # text being typed


def draw_toolbar():
    pygame.draw.rect(screen, (230, 230, 235), (0, 0, WIDTH, TOOLBAR_H))

    # tool buttons
    for i, tool in enumerate(TOOLS):
        rect = pygame.Rect(10 + i * 75, 10, 70, 30)
        bg = (180, 180, 250) if tool == current_tool else (210, 210, 215)
        pygame.draw.rect(screen, bg, rect)
        pygame.draw.rect(screen, (100, 100, 100), rect, 2)
        screen.blit(font.render(tool, True, (30, 30, 30)),
                    font.render(tool, True, (30, 30, 30)).get_rect(center=rect.center))

    # brush size buttons
    for i, size in enumerate(["S", "M", "L"]):
        rect = pygame.Rect(10 + i * 40, 45, 35, 22)
        bg = (180, 180, 250) if size == brush_label else (210, 210, 215)
        pygame.draw.rect(screen, bg, rect)
        pygame.draw.rect(screen, (100, 100, 100), rect, 2)
        screen.blit(font.render(size, True, (30, 30, 30)),
                    font.render(size, True, (30, 30, 30)).get_rect(center=rect.center))

    # color squares on the right
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(WIDTH - (len(COLORS) - i) * 32 - 10, 10, 26, 50)
        pygame.draw.rect(screen, color, rect)
        border = 3 if color == current_color else 1
        pygame.draw.rect(screen, (30, 30, 30), rect, border)


def tool_at(pos):
    for i, tool in enumerate(TOOLS):
        rect = pygame.Rect(10 + i * 75, 10, 70, 30)
        if rect.collidepoint(pos):
            return tool
    return None


def brush_at(pos):
    for i, size in enumerate(["S", "M", "L"]):
        rect = pygame.Rect(10 + i * 40, 45, 35, 22)
        if rect.collidepoint(pos):
            return size
    return None


def color_at(pos):
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(WIDTH - (len(COLORS) - i) * 32 - 10, 10, 26, 50)
        if rect.collidepoint(pos):
            return color
    return None


def canvas_pos(pos):
    return (pos[0], pos[1] - TOOLBAR_H)


def draw_shape(surface, tool, start, end, color, thickness):
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    if tool == "line":
        pygame.draw.line(surface, color, start, end, thickness)
    elif tool == "rect":
        pygame.draw.rect(surface, color, pygame.Rect(min(x1, x2), min(y1, y2), abs(dx), abs(dy)), thickness)
    elif tool == "circle":
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        r = max(2, int((dx * dx + dy * dy) ** 0.5 / 2))
        pygame.draw.circle(surface, color, (cx, cy), r, thickness)
    elif tool == "square":
        side = max(abs(dx), abs(dy))
        sx = 1 if dx >= 0 else -1
        sy = 1 if dy >= 0 else -1
        pygame.draw.rect(surface, color,
                         pygame.Rect(min(x1, x1 + sx * side), min(y1, y1 + sy * side), side, side),
                         thickness)
    elif tool == "right_tri":
        pygame.draw.polygon(surface, color, [(x1, y1), (x2, y1), (x1, y2)], thickness)
    elif tool == "equi_tri":
        base = abs(dx)
        height = base * (math.sqrt(3) / 2)
        mid = (x1 + x2) // 2
        apex_y = y1 - height if dy > 0 else y1 + height
        pygame.draw.polygon(surface, color, [(x1, y1), (x2, y1), (mid, int(apex_y))], thickness)
    elif tool == "rhombus":
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        pts = [(cx, min(y1, y2)), (max(x1, x2), cy), (cx, max(y1, y2)), (min(x1, x2), cy)]
        pygame.draw.polygon(surface, color, pts, thickness)


def flood_fill(surface, start_pos, new_color):
    """Simple BFS flood fill — replaces target color region with new_color."""
    sx, sy = start_pos
    if not (0 <= sx < surface.get_width() and 0 <= sy < surface.get_height()):
        return
    target = surface.get_at((sx, sy))[:3]
    new_rgb = new_color[:3]
    if target == new_rgb:
        return
    queue = deque([(sx, sy)])
    w, h = surface.get_width(), surface.get_height()
    surface.lock()
    while queue:
        x, y = queue.popleft()
        if not (0 <= x < w and 0 <= y < h):
            continue
        if surface.get_at((x, y))[:3] != target:
            continue
        surface.set_at((x, y), new_rgb)
        queue.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    surface.unlock()


def save_canvas():
    name = f"canvas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    pygame.image.save(canvas, name)
    print(f"Saved as {name}")


SHAPE_TOOLS = ("line", "rect", "circle", "square", "right_tri", "equi_tri", "rhombus")

running = True
drawing = False

while running:
    for event in pygame.event.get():
        thickness = BRUSH_SIZES[brush_label]

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # 1, 2, 3 — switch brush sizes
            if event.key == pygame.K_1:
                brush_label = "S"
            elif event.key == pygame.K_2:
                brush_label = "M"
            elif event.key == pygame.K_3:
                brush_label = "L"
            # Ctrl+S → save canvas
            elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                save_canvas()
            # Text tool: typing characters into the buffer
            elif current_tool == "text" and text_pos is not None:
                if event.key == pygame.K_RETURN:
                    # commit the typed text to the canvas
                    text_surf = big_font.render(text_buffer, True, current_color)
                    canvas.blit(text_surf, text_pos)
                    text_pos = None
                    text_buffer = ""
                elif event.key == pygame.K_ESCAPE:
                    text_pos = None
                    text_buffer = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                elif event.unicode:
                    text_buffer += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if my < TOOLBAR_H:
                t = tool_at(event.pos)
                if t is not None:
                    current_tool = t
                b = brush_at(event.pos)
                if b is not None:
                    brush_label = b
                c = color_at(event.pos)
                if c is not None:
                    current_color = c
            else:
                pos = canvas_pos(event.pos)
                if current_tool == "fill":
                    flood_fill(canvas, pos, current_color)
                elif current_tool == "text":
                    text_pos = pos
                    text_buffer = ""
                else:
                    drawing = True
                    last_pos = pos
                    shape_start = pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing and event.pos[1] >= TOOLBAR_H:
                end = canvas_pos(event.pos)
                if current_tool in SHAPE_TOOLS and shape_start:
                    draw_shape(canvas, current_tool, shape_start, end, current_color, thickness)
            drawing = False
            last_pos = None
            shape_start = None

        elif event.type == pygame.MOUSEMOTION and drawing:
            if event.pos[1] < TOOLBAR_H:
                continue
            pos = canvas_pos(event.pos)
            if current_tool == "pencil":
                if last_pos:
                    pygame.draw.line(canvas, current_color, last_pos, pos, thickness)
                last_pos = pos
            elif current_tool == "eraser":
                if last_pos:
                    pygame.draw.line(canvas, (255, 255, 255), last_pos, pos, thickness * 4)
                last_pos = pos

    screen.blit(canvas, (0, TOOLBAR_H))
    draw_toolbar()

    # shape preview
    if drawing and shape_start and current_tool in SHAPE_TOOLS:
        if pygame.mouse.get_pos()[1] >= TOOLBAR_H:
            preview = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H), pygame.SRCALPHA)
            draw_shape(preview, current_tool, shape_start, canvas_pos(pygame.mouse.get_pos()),
                       current_color, 1)
            screen.blit(preview, (0, TOOLBAR_H))

    # text being typed (live preview)
    if current_tool == "text" and text_pos is not None:
        text_surf = big_font.render(text_buffer + "|", True, current_color)
        screen.blit(text_surf, (text_pos[0], text_pos[1] + TOOLBAR_H))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

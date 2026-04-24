import pygame                                # game library
import math                                  # for sqrt used in equilateral triangle

pygame.init()

WIDTH = 900
HEIGHT = 600
TOOLBAR_H = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("Arial", 14, bold=True)
clock = pygame.time.Clock()

COLORS = [
    (0, 0, 0), (255, 255, 255),
    (220, 30, 30), (30, 150, 30), (30, 100, 220),
    (240, 200, 40), (200, 40, 200), (40, 200, 200), (255, 140, 0),
]

# Practice 10 tools + new shapes from Practice 11
TOOLS = ["pen", "rect", "circle", "eraser",
         "square", "right_tri", "equi_tri", "rhombus"]

current_color = COLORS[0]
current_tool = "pen"
brush_size = 4

last_pos = None
shape_start = None


def draw_toolbar():
    pygame.draw.rect(screen, (230, 230, 235), (0, 0, WIDTH, TOOLBAR_H))

    # tool buttons (8 buttons total)
    for i, tool in enumerate(TOOLS):
        rect = pygame.Rect(10 + i * 75, 10, 70, 40)
        bg = (180, 180, 250) if tool == current_tool else (210, 210, 215)
        pygame.draw.rect(screen, bg, rect)
        pygame.draw.rect(screen, (100, 100, 100), rect, 2)
        label = font.render(tool, True, (30, 30, 30))
        screen.blit(label, label.get_rect(center=rect.center))

    # color squares on the right
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(WIDTH - (len(COLORS) - i) * 32 - 10, 10, 26, 40)
        pygame.draw.rect(screen, color, rect)
        border = 3 if color == current_color else 1
        pygame.draw.rect(screen, (30, 30, 30), rect, border)


def tool_at(pos):
    for i, tool in enumerate(TOOLS):
        rect = pygame.Rect(10 + i * 75, 10, 70, 40)
        if rect.collidepoint(pos):
            return tool
    return None


def color_at(pos):
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(WIDTH - (len(COLORS) - i) * 32 - 10, 10, 26, 40)
        if rect.collidepoint(pos):
            return color
    return None


def canvas_pos(pos):
    x, y = pos
    return (x, y - TOOLBAR_H)


def draw_shape(surface, tool, start, end, color, thickness):
    """Draw any of the supported shapes from a start to end point."""
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1

    if tool == "rect":
        rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(dx), abs(dy))
        pygame.draw.rect(surface, color, rect, thickness)

    elif tool == "circle":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        r = max(2, int(((dx) ** 2 + (dy) ** 2) ** 0.5 / 2))
        pygame.draw.circle(surface, color, (cx, cy), r, thickness)

    elif tool == "square":
        # square: side = max of |dx|, |dy|, drawn in the direction of the drag
        side = max(abs(dx), abs(dy))
        sign_x = 1 if dx >= 0 else -1
        sign_y = 1 if dy >= 0 else -1
        rect = pygame.Rect(min(x1, x1 + sign_x * side),
                           min(y1, y1 + sign_y * side),
                           side, side)
        pygame.draw.rect(surface, color, rect, thickness)

    elif tool == "right_tri":
        # right triangle with the right angle at the start corner
        p1 = (x1, y1)              # right angle here
        p2 = (x2, y1)              # along the x axis
        p3 = (x1, y2)              # along the y axis
        pygame.draw.polygon(surface, color, [p1, p2, p3], thickness)

    elif tool == "equi_tri":
        # equilateral triangle: base from (x1, y1) to (x2, y1), apex above the midpoint
        base = abs(dx)
        height = base * (math.sqrt(3) / 2)         # height = base * √3 / 2
        mid_x = (x1 + x2) // 2
        # apex goes above if dragged down, below if dragged up
        apex_y = y1 - height if dy > 0 else y1 + height
        p1 = (x1, y1)
        p2 = (x2, y1)
        p3 = (mid_x, int(apex_y))
        pygame.draw.polygon(surface, color, [p1, p2, p3], thickness)

    elif tool == "rhombus":
        # rhombus inscribed in the bounding box: 4 vertices at the box midpoints
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        top = (cx, min(y1, y2))
        bottom = (cx, max(y1, y2))
        left = (min(x1, x2), cy)
        right = (max(x1, x2), cy)
        pygame.draw.polygon(surface, color, [top, right, bottom, left], thickness)


# all click-and-drag tools (the freehand pen / eraser are not in this list)
SHAPE_TOOLS = ("rect", "circle", "square", "right_tri", "equi_tri", "rhombus")

running = True
drawing = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if my < TOOLBAR_H:
                # click on toolbar → pick a tool or color
                tool = tool_at(event.pos)
                if tool is not None:
                    current_tool = tool
                color = color_at(event.pos)
                if color is not None:
                    current_color = color
            else:
                # click on canvas → start drawing
                drawing = True
                last_pos = canvas_pos(event.pos)
                shape_start = last_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing and my >= TOOLBAR_H:
                end = canvas_pos(event.pos)
                # commit the shape to the canvas
                if current_tool in SHAPE_TOOLS and shape_start:
                    draw_shape(canvas, current_tool, shape_start, end, current_color, brush_size)
            drawing = False
            last_pos = None
            shape_start = None

        elif event.type == pygame.MOUSEMOTION and drawing:
            if event.pos[1] < TOOLBAR_H:
                continue
            pos = canvas_pos(event.pos)
            if current_tool == "pen":
                if last_pos:
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                last_pos = pos
            elif current_tool == "eraser":
                if last_pos:
                    pygame.draw.line(canvas, (255, 255, 255), last_pos, pos, brush_size * 4)
                last_pos = pos

    screen.blit(canvas, (0, TOOLBAR_H))
    draw_toolbar()

    # live shape preview while dragging
    if drawing and shape_start and current_tool in SHAPE_TOOLS:
        mx, my = pygame.mouse.get_pos()
        if my >= TOOLBAR_H:
            end = canvas_pos((mx, my))
            preview = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H), pygame.SRCALPHA)
            draw_shape(preview, current_tool, shape_start, end, current_color, 1)
            screen.blit(preview, (0, TOOLBAR_H))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

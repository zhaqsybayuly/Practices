import pygame                                # game library

pygame.init()                                # start pygame

WIDTH = 800                                  # window width
HEIGHT = 600                                 # window height
TOOLBAR_H = 60                               # height of the top bar with tools and colors

screen = pygame.display.set_mode((WIDTH, HEIGHT))   # create the window
pygame.display.set_caption("Paint")          # window title

# the canvas is a separate Surface that holds all the drawings.
# we draw it under the toolbar every frame, so the art is never lost.
canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_H))
canvas.fill((255, 255, 255))                 # start with a white canvas

font = pygame.font.SysFont("Arial", 16, bold=True)   # font used for the tool labels
clock = pygame.time.Clock()                  # for controlling FPS

# colors the user can pick from (shown on the right of the toolbar)
COLORS = [
    (0, 0, 0),          # black
    (255, 255, 255),    # white
    (220, 30, 30),      # red
    (30, 150, 30),      # green
    (30, 100, 220),     # blue
    (240, 200, 40),     # yellow
    (200, 40, 200),     # purple
    (40, 200, 200),     # cyan
    (255, 140, 0),      # orange
]

TOOLS = ["pen", "rect", "circle", "eraser"]   # tool names shown on the left

current_color = COLORS[0]                    # active color (starts black)
current_tool = "pen"                         # active tool (starts with the pen)
brush_size = 4                               # line thickness for pen / shape outlines

last_pos = None                              # last mouse position (used to draw smooth strokes)
shape_start = None                           # corner where the user pressed for rect/circle


def draw_toolbar():
    pygame.draw.rect(screen, (230, 230, 235), (0, 0, WIDTH, TOOLBAR_H))   # toolbar background

    # draw the tool buttons on the left
    for i, tool in enumerate(TOOLS):
        rect = pygame.Rect(10 + i * 70, 10, 60, 40)                # position of this button
        # highlight the button if this tool is currently selected
        bg = (180, 180, 250) if tool == current_tool else (210, 210, 215)
        pygame.draw.rect(screen, bg, rect)                         # button background
        pygame.draw.rect(screen, (100, 100, 100), rect, 2)         # button border
        label = font.render(tool, True, (30, 30, 30))              # tool name text
        screen.blit(label, label.get_rect(center=rect.center))     # center the text inside the button

    # draw the color palette on the right
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(WIDTH - (len(COLORS) - i) * 40 - 10, 10, 32, 40)   # position
        pygame.draw.rect(screen, color, rect)                                  # filled color square
        border = 3 if color == current_color else 1                            # thicker border if selected
        pygame.draw.rect(screen, (30, 30, 30), rect, border)


def tool_at(pos):
    # return the tool name if the mouse click landed on one of the tool buttons
    for i, tool in enumerate(TOOLS):
        rect = pygame.Rect(10 + i * 70, 10, 60, 40)
        if rect.collidepoint(pos):
            return tool
    return None


def color_at(pos):
    # return the color if the mouse click landed on one of the color squares
    for i, color in enumerate(COLORS):
        rect = pygame.Rect(WIDTH - (len(COLORS) - i) * 40 - 10, 10, 32, 40)
        if rect.collidepoint(pos):
            return color
    return None


def canvas_pos(pos):
    # convert screen coordinates to canvas coordinates
    # (the canvas starts right below the toolbar, so subtract the toolbar height)
    x, y = pos
    return (x, y - TOOLBAR_H)


running = True                               # main loop flag
drawing = False                              # True while the mouse button is held on the canvas

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:        # user closed the window
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos               # position where the mouse was pressed
            if my < TOOLBAR_H:
                # click on the toolbar → pick a tool or a color
                tool = tool_at(event.pos)
                if tool is not None:
                    current_tool = tool
                color = color_at(event.pos)
                if color is not None:
                    current_color = color
            else:
                # click on the canvas → start drawing
                drawing = True
                last_pos = canvas_pos(event.pos)     # remember where we started
                shape_start = last_pos               # same point is the shape's starting corner

        elif event.type == pygame.MOUSEBUTTONUP:
            # mouse released → if we were drawing a shape, commit it to the canvas
            if drawing and my >= TOOLBAR_H:
                end = canvas_pos(event.pos)          # where the shape ends
                if current_tool == "rect" and shape_start:
                    x1, y1 = shape_start
                    x2, y2 = end
                    # build a rect from the two corners, no matter which way we dragged
                    rect = pygame.Rect(min(x1, x2), min(y1, y2),
                                       abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(canvas, current_color, rect, brush_size)
                elif current_tool == "circle" and shape_start:
                    x1, y1 = shape_start
                    x2, y2 = end
                    cx = (x1 + x2) // 2              # center x
                    cy = (y1 + y2) // 2              # center y
                    # radius = half the distance between start and end points
                    r = max(2, int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 / 2))
                    pygame.draw.circle(canvas, current_color, (cx, cy), r, brush_size)
            drawing = False
            last_pos = None
            shape_start = None

        elif event.type == pygame.MOUSEMOTION and drawing:
            # don't draw while the mouse is still on the toolbar
            if event.pos[1] < TOOLBAR_H:
                continue
            pos = canvas_pos(event.pos)              # current canvas position
            if current_tool == "pen":
                # draw a line from the previous position to the current one → smooth stroke
                if last_pos:
                    pygame.draw.line(canvas, current_color, last_pos, pos, brush_size)
                last_pos = pos                       # update last position for the next segment
            elif current_tool == "eraser":
                # eraser is just a thick white pen
                if last_pos:
                    pygame.draw.line(canvas, (255, 255, 255), last_pos, pos, brush_size * 4)
                last_pos = pos

    # draw the canvas onto the screen, right below the toolbar
    screen.blit(canvas, (0, TOOLBAR_H))
    draw_toolbar()                                   # toolbar goes on top every frame

    # live preview while the user is dragging a rect or circle.
    # we draw it only on the screen — it gets committed to the canvas on MOUSEBUTTONUP.
    if drawing and shape_start and current_tool in ("rect", "circle"):
        mx, my = pygame.mouse.get_pos()              # current mouse position
        if my >= TOOLBAR_H:
            end = canvas_pos((mx, my))
            x1, y1 = shape_start
            x2, y2 = end
            if current_tool == "rect":
                rect = pygame.Rect(min(x1, x2), min(y1, y2) + TOOLBAR_H,
                                   abs(x2 - x1), abs(y2 - y1))
                pygame.draw.rect(screen, current_color, rect, 1)   # thin preview outline
            else:
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                r = max(2, int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 / 2))
                pygame.draw.circle(screen, current_color, (cx, cy + TOOLBAR_H), r, 1)

    pygame.display.flip()                            # show the frame
    clock.tick(60)                                   # cap at 60 FPS

pygame.quit()                                        # close pygame

import pygame


class Ball:
    RADIUS = 25
    STEP = 20
    COLOR = (255, 0, 0)

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = screen_width // 2
        self.y = screen_height // 2

    def move(self, direction):
        # only apply the move if the new position stays fully on screen
        if direction == "left" and self.x - self.STEP - self.RADIUS >= 0:
            self.x -= self.STEP
        elif direction == "right" and self.x + self.STEP + self.RADIUS <= self.screen_width:
            self.x += self.STEP
        elif direction == "up" and self.y - self.STEP - self.RADIUS >= 0:
            self.y -= self.STEP
        elif direction == "down" and self.y + self.STEP + self.RADIUS <= self.screen_height:
            self.y += self.STEP

    def draw(self, surface):
        pygame.draw.circle(surface, self.COLOR, (self.x, self.y), self.RADIUS)

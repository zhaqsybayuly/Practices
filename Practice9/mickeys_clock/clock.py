import pygame
import io
from datetime import datetime
import cairosvg


def load_svg(path, size):
    png_bytes = cairosvg.svg2png(url=path, output_width=size, output_height=size)
    return pygame.image.load(io.BytesIO(png_bytes)).convert_alpha()


class MickeyClock:
    # arms point horizontally in the SVG files, so the default clockwise angle
    # from 12 is 90° for the right arm and 270° for the left arm
    RIGHT_DEFAULT = 90
    LEFT_DEFAULT = 270
    BODY_SCALE = 0.6

    def __init__(self, size):
        self.size = size
        self.center = (size // 2, size // 2)

        self.face = load_svg("images/clock_face.svg", size)
        self.right_arm = load_svg("images/right_arm.svg", size)
        self.left_arm = load_svg("images/left_arm.svg", size)
        self.pin = load_svg("images/pin.svg", size)

        # shrink the body so it doesn't overlap the numbers
        body_full = load_svg("images/body.svg", size)
        body_size = int(size * self.BODY_SCALE)
        self.body = pygame.transform.smoothscale(body_full, (body_size, body_size))
        self.body_rect = self.body.get_rect(center=self.center)

    def _blit_rotated(self, surface, image, angle_deg):
        rotated = pygame.transform.rotate(image, angle_deg)
        rect = rotated.get_rect(center=self.center)
        surface.blit(rotated, rect)

    def draw(self, surface):
        now = datetime.now()
        minute_cw = now.minute * 6
        second_cw = now.second * 6

        # pygame rotates CCW on positive angles, so subtract from default
        right_rotation = self.RIGHT_DEFAULT - minute_cw
        left_rotation = self.LEFT_DEFAULT - second_cw

        surface.blit(self.face, (0, 0))
        surface.blit(self.body, self.body_rect)
        self._blit_rotated(surface, self.right_arm, right_rotation)   # minutes
        self._blit_rotated(surface, self.left_arm, left_rotation)     # seconds
        surface.blit(self.pin, (0, 0))


from imports import *
from pygame import gfxdraw


class Dot:
    mag = 4
    def __init__(self, x, y, color, radius=20):
        self.x = x
        self.y = y
        self.color = color
        self.r = radius

        self.w = ceil(self.r * 2 + 1)
        self.h = ceil(self.r * 2 + 1)
        self.mag_w, self.mag_h, self.mag_r = self.w * self.mag, self.h * self.mag, self.r * self.mag
        self.mag_surface = pg.Surface((self.mag_w, self.mag_h), pg.SRCALPHA, 32)

    @property
    def surface(self):
        return pg.transform.smoothscale(self.mag_surface, (self.w, self.h))

    def setup_surface(self):
        top, left = self.y - self.r, self.x - self.r
        yf = top - floor(top)
        xf = left - floor(left)
        x_offset = round(xf * self.mag)
        y_offset = round(yf * self.mag)

        self.mag_surface.fill(COLOR_TRANSPARENT)
        pg.draw.circle(self.mag_surface, self.color, (self.mag_r + x_offset, self.mag_r + y_offset), self.mag_r)

    def draw(self, surface):
        self.setup_surface()
        top, left = self.y - self.r, self.x - self.r
        surface.blit(self.surface, (floor(left), floor(top)))



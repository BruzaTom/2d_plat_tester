from scripts.fonts import Font
from scripts.utils import load_image
import pygame

class Hud:
    def __init__(self, game):
        self.game = game
        self.small_font = Font('data/fonts/small_font/black.png')
        self.heart_img = load_image('hearts/heart.png')
        self.empty_heart_img = load_image('hearts/empty_heart.png')
        self.max_health = self.game.player.health

    def blit_hearts(self, surface):
        for i in range(0, self.max_health):
            x_pos = (i + 1) * self.heart_img.get_width()
            if i >= self.game.player.health:
                surface.blit(self.empty_heart_img, (x_pos, 20))
            else:
                surface.blit(self.heart_img, (x_pos, 20))

    def render(self, surface):
        self.blit_hearts(surface)


import pygame
from scripts.utils import load_image
from scripts.words import Chest_opened

class Chest:
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.closed = load_image('tiles/stations/chests/closed_chest.png')
        self.opened = load_image('tiles/stations/chests/open_chest.png')
        self.image = self.closed
        self.triggered = False

    def update(self):
        if self.game.player.rect().colliderect(self.image.get_rect(topleft=(self.pos[0], self.pos[1]))) and self.game.key_count > 0:
            if not self.triggered:
                self.game.key_count -= 1
                self.game.words.append(Chest_opened(self.game, self.pos.copy()))
                self.image = self.opened
                self.triggered = True
                self.game.sfx['open_chest'].play(0)


    def render(self, surface, offset=(0, 0)):
        pos_offset_p_ani_x = self.pos[0] - offset[0] 
        pos_offset_p_ani_y = self.pos[1] - offset[1]
        surface.blit(self.image, (pos_offset_p_ani_x, pos_offset_p_ani_y))

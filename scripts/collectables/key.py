import pygame
from scripts.utils import load_image

class Key:
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.img = load_image('tiles/collectables/key.png')

    def update(self):
        if self.game.player.rect().collidepoint(self.pos):
            return True

    def render(self, surface, offset=(0, 0)):
        pos_offset_p_ani_x = self.pos[0] - offset[0] 
        pos_offset_p_ani_y = self.pos[1] - offset[1]
        surface.blit(self.img, (pos_offset_p_ani_x, pos_offset_p_ani_y))

        
        


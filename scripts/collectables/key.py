import pygame
from scripts.utils import load_image, get_img_rect
from scripts.words import Plus_key

class Key:
    def __init__(self, game, pos):
        self.game = game
        self.pos = pos
        self.img = load_image('tiles/collectables/key.png')
        self.img_rect = get_img_rect(self.img, self.pos)

    def update(self):
        if self.game.player.rect().colliderect(self.img_rect):
            self.game.words.append(Plus_key(self.game, self.pos.copy()))
            return True

    def render(self, surface, offset=(0, 0)):
        pos_offset_p_ani_x = self.pos[0] - offset[0] 
        pos_offset_p_ani_y = self.pos[1] - offset[1]
        surface.blit(self.img, (pos_offset_p_ani_x, pos_offset_p_ani_y))

        
        


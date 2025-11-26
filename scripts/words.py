import pygame
from scripts.utils import Animation, load_images

class Word:
    def __init__(self, game, pos):
        self.animation = None #overwritten in children
        self.pos = pos
        self.img = None
        self.timer = 0

    def update(self):
        self.animation.update() 
        self.pos[1] -= .5
        self.timer += .10

    def render(self, surface, offset=(0, 0)):
        pos_offset_p_ani_x = self.pos[0] - offset[0] 
        pos_offset_p_ani_y = self.pos[1] - offset[1]
        surface.blit(self.animation.img(), (pos_offset_p_ani_x, pos_offset_p_ani_y))

class Plus_key(Word):
    def __init__(self, game, pos):
        super().__init__(game, pos)        
        self.animation = Animation(load_images("words/plus_key"))
        
class Chest_opened(Word):
    def __init__(self, game, pos):
        super().__init__(game, pos)        
        self.animation = Animation(load_images("words/chest_opened"))



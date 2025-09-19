#[[x, y], direction, timer]
from scripts.utils import blit_box
import pygame

class Projectile:
    def __init__(self, game, pos, size, direction, animation, flip):
        self.pos = pos
        self.size = size
        self.direction = direction
        self.timer = 0
        self.animation = animation
        self.point = (0, 0)
        self.flip = flip
        self.image = None
        self.ani_offset = (0, 0)
        self.offset_pos = (0, 0)
        
    def update(self):
        self.pos[0] += self.direction#[[x, y], direction, timer]
        self.timer += 1
        self.animation.update()
        if not self.flip:
            self.image = pygame.transform.flip(self.animation.img(), True, False)
            self.ani_offset = (-11, 0)
        else:
            self.image = self.animation.img()
            self.ani_offset = (11, 0)
        
    def render(self, surface, offset=(0, 0)):
        img = self.animation.img()
        pos_x = self.pos[0] - img.get_width() / 2 - offset[0]
        pos_y = self.pos[1] - img.get_height() / 2 - offset[1]
        self.point = (pos_x, pos_y)#for collisions
        offset_pos = (self.point[0] + self.ani_offset[0], self.point[1])
        surface.blit(self.image, offset_pos)
        blit_box(surface, self.point, img.get_size(), 'red')#use point and image.get_size


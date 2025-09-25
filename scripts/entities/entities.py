import pygame, math, random
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.utils import blit_box
from scripts.projectile import Projectile

class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        #if using baisic py not pyce
        self.pos = list(pos)#force convert list
        self.size = size
        self.velocity = [0, 0]
        #keep track of collisions, usefule like walljumnping
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        self.action = ''
        self.ani_offset = (-3, -3)
        self.flip = False
        self.set_action('idle')
        self.last_movement = [0, 0]

    def set_action(self, action):
        if action != self.action:
            self.action = action
            #set animation object from game
            self.animation = self.game.assets[self.type + '/' + self.action].copy()

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        #keep track of collisions, usefule like walljumnping
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}

        frame_movement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])
        #movement and collisions work togethr
        #check rects around player x pos for collisions
        #then move player pos if possible
        self.pos[0] += frame_movement[0]
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.pos[0] = entity_rect.x
        #check rects around player y pos for collisions
        self.pos[1] += frame_movement[1]
        #new entity_rect or else dosent work
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.pos[1] = entity_rect.y

        #animation flip
        if movement[0] > 0:
            self.flip = False
        if movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        #gravity
        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surface, offset=(0, 0)):
        flip_flagged_img = pygame.transform.flip(self.animation.img(), self.flip, False)
        pos_offset_p_ani_x = self.pos[0] - offset[0] + self.ani_offset[0] 
        pos_offset_p_ani_y = self.pos[1] - offset[1] + self.ani_offset[1] 
        ani_pos_os = (pos_offset_p_ani_x, pos_offset_p_ani_y) 
        #-----------------true pos debug---------------------
        #blit_box(surface, (self.pos[0] - offset[0], self.pos[1] - offset[1]), self.animation.img().get_size(), 'red')
        #blit_box(surface, (self.pos[0] - offset[0], self.pos[1] - offset[1]), self.size, 'red')
        #----------------------------------------------------
        surface.blit(flip_flagged_img, ani_pos_os)
       
       #before animations
        #surface.blit(self.game.assets['player'], (self.pos[0] - offset[0], self.pos[1] - offset[1]))






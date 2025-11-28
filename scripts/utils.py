import pygame
import os

BASE_IMG_PATH = 'data/images/'

#animation class
class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_dur = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_dur, self.loop)

    def update(self):
        if len(self.images) == 1:
            return
        else:
            dur_x_len = self.img_dur * len(self.images) 
            if self.loop:
                self.frame = self.frame + 1 % dur_x_len
            else:
                self.frame = min(self.frame + 1, dur_x_len - 1)
                if self.frame >= dur_x_len - 1:
                    self.done = True

    def img(self):
        index = int(self.frame / self.img_dur) % len(self.images)
        return self.images[index]

#images
def load_image(path):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    #img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    #for all file systems
    for img_name in sorted(os.listdir(BASE_IMG_PATH + path)):
        images.append(load_image(path + '/' + img_name))
        #color_key_debug(images[-1])
    return images

#for collectables and stations collide rects
def get_img_rect(img, pos):
    return img.get_rect(topleft=(pos[0], pos[1]))
    
#debug
def color_key_debug(img):
    print(f'img: {img}\ntop-left pixel: {img.get_at((0, 0))}')

def blit_box(screen, pos, size, color_str):
    rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
    color = pygame.Color(color_str)
    pygame.draw.rect(screen, color, rect, width=1)




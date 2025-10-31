from scripts.fonts import Font
from scripts.utils import load_image
import pygame

class Hud:
    def __init__(self, game):
        self.game = game
        self.player_img = self.game.player.img
        self.small_font = Font('data/fonts/large_font/1.png')
        self.heart_img = load_image('hearts/heart.png')
        self.key_img = load_image('tiles/collectables/key.png')
        self.empty_heart_img = load_image('hearts/empty_heart.png')
        self.max_health = self.game.player.health

    def blit_hearts(self, surface):
        for i in range(0, self.max_health):
            x_pos = (i + 1) * self.heart_img.get_width()
            if i >= self.game.player.health:
                surface.blit(self.empty_heart_img, (x_pos, 20))
            else:
                surface.blit(self.heart_img, (x_pos, 20))

    def blit_keys(self, surface):
        pos = (280, 20)
        surface.blit(self.key_img, pos)
        pos = (pos[0]+20, pos[1]+3)
        self.small_font.render(surface, f'{self.game.key_count}', pos)

    def blit_lives(self, surface):
        pos = (0, 0)
        for i in range(0, self.max_health):
            pos = (pos[0]+(self.player_img.get_width()//2), pos[1])
            surface.blit(self.player_img, pos)



    def render(self, surface):
        self.blit_hearts(surface)
        self.blit_keys(surface)
        self.blit_lives(surface)
        #self.info(surface)

    def info(self, surface):
        self.tile_info(surface)
        self.player_info(surface)
        self.game_info(surface)

    def tile_info(self, surface):
        x_pos, y_pos = 200, 20
        self.small_font.render(surface, 'Tile Map:', (x_pos, y_pos))
        y_pos += 10
        self.small_font.render(surface, f'size = {str(self.game.tilemap.tile_size)}', (x_pos, y_pos))
        y_pos += 10
        self.small_font.render(surface, f'tiles_around = {str(len(self.game.tilemap.tile_locs_around))}', (x_pos, y_pos))

    def player_info(self, surface):
        x_pos, y_pos = 500, 20
        self.small_font.render(surface, 'Player:', (x_pos, 20))
        pos = f'({self.game.player.pos[0]:.3f}, {self.game.player.pos[1]:.3f})'
        y_pos += 10
        self.small_font.render(surface, f'pos = ' + pos, (x_pos, y_pos))
        velocity = f'({int(self.game.player.velocity[0])}, {int(self.game.player.velocity[1])})'
        y_pos += 10
        self.small_font.render(surface, f'velocity = ' + velocity, (x_pos, y_pos))
        text = str(self.game.player.animation.images[self.game.player.animation.frame % len(self.game.player.animation.images)])
        y_pos += 10
        self.small_font.render(surface, f'animation = ' + str(self.game.player.action), (x_pos, y_pos))
        y_pos += 10
        self.small_font.render(surface, f'ani_offset = {str(self.game.player.ani_offset)}', (x_pos, y_pos))

    def game_info(self, surface):
        x_pos, y_pos = 300, 20
        self.small_font.render(surface, 'Game:', (x_pos, y_pos))
        y_pos += 10
        self.small_font.render(surface, f'key_count = {self.game.key_count}', (x_pos, y_pos))
        y_pos += 10
        self.small_font.render(surface, f'enemy count = {len(self.game.enemies)}', (x_pos, y_pos))



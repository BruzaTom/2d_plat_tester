import sys
import pygame
from utils import load_images
from tilemap import TileMap

RENDER_SCALE = 2.0

class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Editor')
        #game screen
        sw, sh = 640, 480
        self.screen = pygame.display.set_mode((640, 480))
        #render size 'zoom'
        self.display = pygame.Surface((320, 240))
        #
        self.clock = pygame.time.Clock()

        self.assets = {
                #from scripts/utils.py
                'decor' : load_images('tiles/decor'),
                'grass' : load_images('tiles/grass'),
                'large_decor' : load_images('tiles/large_decor'),
                'stone' : load_images('tiles/stone'),
                'spawners' : load_images('tiles/spawners'),
                'empty' : load_images('tiles/empty'),
                }
        
        #movement left, right, up, down
        self.movement = [False, False, False, False]
        #tilemap
        self.tilemap = TileMap(self, 32)
        try:
            self.tilemap.load('map.json')
        except FileNotFoundError:
            pass
        #camera scroll
        self.scroll = [0, 0]

        self.tile_lst = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        #input flags
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.ongrid = True

    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            #scroll camera based on movements left, right, up, down
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            #render tiles
            self.tilemap.render(self.display, offset=render_scroll)
            #tile img preview
            tile_group = self.tile_lst[self.tile_group]
            current_tile_img = self.assets[tile_group][self.tile_variant].copy()
            current_tile_img.set_alpha(100)
            #mouse position
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)

            #formula for tile pos
            mpos_scroll_x_div_tile_size = int(mpos[0] + self.scroll[0]) // self.tilemap.tile_size
            mpos_scroll_y_div_tile_size = int(mpos[1] + self.scroll[1]) // self.tilemap.tile_size
            tile_pos = (mpos_scroll_x_div_tile_size, mpos_scroll_y_div_tile_size)
            if self.ongrid:
                #display tile preview at scroll
                tile_pos_x_by_size_min_scroll = tile_pos[0] * self.tilemap.tile_size - self.scroll[0]
                tile_pos_y_by_size_min_scroll = tile_pos[1] * self.tilemap.tile_size - self.scroll[1]
                tile_scroll = (tile_pos_x_by_size_min_scroll, tile_pos_y_by_size_min_scroll)
                self.display.blit(current_tile_img, tile_scroll)
            else:
                self.display.blit(current_tile_img, mpos)

            #assighn new tile
            if self.clicking and self.ongrid:
                tile_pos_key = str(tile_pos[0]) + ';' + str(tile_pos[1])
                render_tile = {'type': tile_group, 'variant': self.tile_variant, 'pos': tile_pos}
                self.tilemap.tilemap[tile_pos_key] = render_tile
            #remove tiles
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tilemap.tilemap:
                    del self.tilemap.tilemap[tile_loc]
                #un optimized
                for tile in self.tilemap.offgrid_tiles.copy():
                    #convert world space to display space so - scroll
                    tile_pos_x = tile['pos'][0] - self.scroll[0] 
                    tile_pos_y = tile['pos'][1] - self.scroll[1] 
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile_pos_x, tile_pos_y, tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tilemap.offgrid_tiles.remove(tile)

            #top right tile indicator
            self.display.blit(current_tile_img, (5, 5))

            #input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.ongrid:#place offgrid tile
                            tile_pos_x = mpos[0] + self.scroll[0] 
                            tile_pos_y = mpos[1] + self.scroll[1] 
                            tile_pos = (tile_pos_x , tile_pos_y)
                            render_tile = {'type': tile_group, 'variant': self.tile_variant, 'pos': tile_pos}
                            self.tilemap.offgrid_tiles.append(render_tile)
                    if event.button == 3:
                        self.right_clicking = True
                if event.type == pygame.MOUSEWHEEL:
                    if self.shift:
                        if event.y > 0:
                            self.tile_variant = (self.tile_variant - 1) % len(self.assets[tile_group])
                        elif event.y < 0:
                            self.tile_variant = (self.tile_variant + 1) % len(self.assets[tile_group])
                    else:
                        if event.y > 0:
                            self.tile_group = (self.tile_group - 1) % len(self.tile_lst)
                            self.tile_variant = 0
                        elif event.y < 0:
                            self.tile_group = (self.tile_group + 1) % len(self.tile_lst)
                            self.tile_variant = 0
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False


                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:#left
                        self.movement[0] = True
                    if event.key == pygame.K_d:#right
                        self.movement[1] = True
                    if event.key == pygame.K_w:#up
                        self.movement[2] = True
                    if event.key == pygame.K_s:#down
                        self.movement[3] = True
                    if event.key == pygame.K_g:#on grid switch
                        self.ongrid = not self.ongrid
                    if event.key == pygame.K_o:#save
                        self.tilemap.save('map.json')
                    if event.key == pygame.K_LSHIFT:#shift
                        self.shift = True
                    if event.key == pygame.K_t:#auto tile
                        self.tilemap.autotile()
                        print('saved to map.json')
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False
                    if event.key == pygame.K_LSHIFT:
                        self.shift = False
            #finishers
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Editor().run()

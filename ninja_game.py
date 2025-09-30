import sys, os
import random#partickles
import math#particles
import pygame
from scripts.entities.players import Samurai2, Player, Samuri
from scripts.entities.enemy import Enemy
from scripts.utils import load_image, load_images, Animation, blit_box
from scripts.tilemap import TileMap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.hud import Hud
from scripts.collectables.key import Key

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('ninja game')
        #game screen
        self.screen = pygame.display.set_mode((1400, 900))
        #render size 'zoom' / 'camera' - both displays will merge seperating outlined from normal
        render_size = (self.screen.get_width() // 4, self.screen.get_height() // 4)
        self.display = pygame.Surface((640, 480), pygame.SRCALPHA)#objects withoutline
        self.display_2 = pygame.Surface((640, 480))#objects without outline
        #
        self.clock = pygame.time.Clock()
        #movement x y
        self.movement = [False, False]

        self.assets = {
                #from scripts/utils.py
                'portals': load_images('tiles/portals'),
                'decor' : load_images('tiles/decor'),
                'grass' : load_images('tiles/grass'),
                'large_decor' : load_images('tiles/large_decor'),
                'stone' : load_images('tiles/stone'),
                'empty' : load_images('tiles/empty'),
                'blue' : load_images('tiles/blue'),
                'player' : load_image('entities/player.png'),
                'background' : load_image('background2.png'),
                'clouds': load_images('clouds'),
                'collectables': load_images('tiles/collectables'),
                'enemy/idle': Animation(load_images('entities/enemy/idle'), img_dur=6),
                'enemy/run': Animation(load_images('entities/enemy/run'), img_dur=4),
                'enemy/projectile': Animation(load_images('entities/enemy/projectile'), img_dur=20),
                'particle/leaf': Animation(load_images('particles/leaf'), img_dur=20, loop=False),
                'particle/particle': Animation(load_images('particles/particle'), img_dur=6, loop=False),
                'gun': load_image('gun.png'),
                }

        #sound effects
        self.sfx = {
                'jump': pygame.mixer.Sound('data/sfx/jump.wav'),
                'dash': pygame.mixer.Sound('data/sfx/dash.wav'),
                'hit': pygame.mixer.Sound('data/sfx/hit.wav'),
                'shoot': pygame.mixer.Sound('data/sfx/shoot.wav'),
                'ambience': pygame.mixer.Sound('data/sfx/ambience.wav'),
                }

        self.sfx['ambience'].set_volume(0.2)
        self.sfx['shoot'].set_volume(0.4)
        self.sfx['hit'].set_volume(0.8)
        self.sfx['dash'].set_volume(0.3)
        self.sfx['jump'].set_volume(0.7)

        self.clouds = Clouds(self.assets['clouds'], count=16)
        #pass in assets to TileMap using self as the game
        self.tilemap = TileMap(self, 30)
        print(self.tilemap.tile_size)

        #start levels
        self.level = 0
        self.load_level()

        #screen-shake effect
        self.screenshake = 0

        self.hud = Hud(self)

    #level loader
    def load_level(self):
        #self.tilemap.load('data/maps/' + str(map_id) + '.json')
        self.tilemap.load('map.json')
        
        #leaf spawners are trees ('large_decor', 2)
        self.leaf_spawners = []
        for tree in self.tilemap.extract([('large_decor', 2)], keep=True):
            self.leaf_spawners.append(pygame.Rect(4 + tree['pos'][0], 4 + tree['pos'][1], 23, 13))

        #keys
        self.keys = []
        for collectable in self.tilemap.extract([('collectables', 0)]):
            self.keys.append(Key(self, collectable['pos']))

        #physics entities spawners
        self.enemies = []
        for spawner in self.tilemap.extract([('spawners', 0), ('spawners', 1)]):
            if spawner['variant'] == 0:
                
                #player select
                #self.player = Samuri(self, spawner['pos'], 10) 
                self.player = Samurai2(self, spawner['pos'], 10) 
                #self.player = Player(self, spawner['pos'], 10) 

                self.player.pos = spawner['pos']
                self.player.air_time = 0#prevents falling to death from multiple triggers
            else:
                self.enemies.append(Enemy(self, spawner['pos'], (8, 15)))
        
        #empty containers
        self.projectiles = []
        self.particles = []
        self.sparks = []
        self.key_count = 0

        #'camera' scroll
        self.scroll = [0, 0]
        #death
        self.dead = 0
        #transition
        self.transition = -30

    #game logic
    def logic(self):
            #--------------------logic------------------------
        #level transition logic
        if not len(self.enemies):#if no more enemies
            self.transition += 1
            if self.transition > 30:
                self.level = min(self.level + 1, len(os.listdir('data/maps')) - 1)
                #self.load_level(self.level)
                self.load_level()
        if self.transition < 0:
            self.transition += 1
        

        #leaf particle logic
        for rect in self.leaf_spawners:
            #49999 makes the particals pass condition less often
            if random.random() * 49999 < rect.width * rect.height:
                pos_x = rect.x + random.random() * rect.width
                pos_y = rect.y + random.random() * rect.height
                pos = (pos_x, pos_y)
                self.particles.append(Particle(self, 'leaf', pos, velocity=[-0.1, 0.3], frame=random.randint(0, 20)))
        
        #screenshake logic
        self.screenshake = max(0, self.screenshake - 1) 

        #render scroll logic
        self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
        self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
        #convert to int to avoid jitters
        render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
        return render_scroll
    
    def run(self):
        #funcs
        def manage_keys():
            for key in self.keys:
                kill = key.update()
                key.render(self.display_2, offset=render_scroll)
                if kill:
                    self.key_count += 1
                    self.keys.remove(key)

        def manage_transition():
            if self.transition:
                transition_surface = pygame.Surface(self.display.get_size())
                radius = (30 - abs(self.transition)) * 8
                x_y = (self.display.get_width() // 2, self.display.get_height() // 2)
                pygame.draw.circle(transition_surface, (255, 255, 255), x_y, radius)
                transition_surface.set_colorkey((255, 255, 255))
                self.display.blit(transition_surface, (0, 0))

        def manage_particles():
            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display_2, offset=render_scroll)
                if particle.p_type == 'leaf':
                    #apply sin effect to position               0.035 slows down effect
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

        #enemy logic
        def manage_enemies():
            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display_2, offset=render_scroll)
                if kill:
                    self.enemies.remove(enemy)

        #enemy projectile logic
        def manage_enemy_projectiles():
            for projectile in self.projectiles.copy():
                projectile.update()
                projectile.render(self.display, offset=render_scroll)
                #debug projectiles
                #blit_box(self.display_2, (pos_x, pos_y), img.get_size(), 'green')
                if self.tilemap.solid_check(projectile.pos):#projectile hit wall
                    self.projectiles.remove(projectile)
                    #add parks
                    for i in range(4):
                        spark_pos = projectile.pos
                        spark_angle = random.random() - 0.5 + (math.pi if projectile.direction > 0 else 0)#bounce off walls
                        spark_speed = 2 + random.random()
                        new_spark = Spark(spark_pos, spark_angle, spark_speed)
                        self.sparks.append(new_spark)
                elif projectile.timer > 720:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile.pos):#projectile hit player
                        self.projectiles.remove(projectile)
                        self.player.health -= 1
                        if self.player.health <= 0:
                            self.dead += 1#start death timer
                        self.sfx['hit'].play(0)
                        #screenshake
                        self.screenshake = max(16, self.screenshake)
                        for i in range(30):#burst effect of sparks and particles
                            #add sparks
                            spark_pos = self.player.rect().center
                            spark_angle = random.random() * math.pi * 2
                            spark_speed = random.random() * 5
                            new_spark = Spark(spark_pos, spark_angle, spark_speed)
                            self.sparks.append(new_spark)
                            #add particles
                            pos = self.player.rect().center
                            velocity_x = math.cos(spark_angle + math.pi) * spark_speed * 0.5
                            velocity_y = math.sin(spark_angle + math.pi) * spark_speed * 0.5
                            particle_velocity = [velocity_x, velocity_y]
                            new_particle = Particle(self, 'particle', pos, velocity=particle_velocity, frame=random.randint(0, 7))
                            self.particles.append(new_particle)

        #death logic
        def manage_death():
            if self.dead:
                self.dead += 1
                if self.dead >= 10:#ensure positive transition is rendered
                    self.transition = min(30, self.transition + 1)#without triggering next level
                if self.dead > 40:
                    self.load_level()

        #sparks from projectiles logic
        def manage_projectile_sparks():
            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset=render_scroll)
                if kill:
                    self.sparks.remove(spark)

        def manage_screenshake():
                mod = (random.random() * self.screenshake) - (self.screenshake / 2)
                return (mod, mod)

        def manage_mask():#wont effect renders called after
            display_mask = pygame.mask.from_surface(self.display)#mask for respective renders
            display_sillouette = display_mask.to_surface(setcolor=(0, 0, 0, 255), unsetcolor=(0, 0, 0, 0))#make less transparent
            self.display_2.blit(display_sillouette, (4, 4))
        
        #bg music
        pygame.mixer.music.load('data/music.wav')
        pygame.mixer.music.set_volume(0.5)
        #pygame.mixer.music.play(-1)#0, 1, -1
        #bg sfx
        #self.sfx['ambience'].play(-1)

        #--------debug assets-----------
        #for key in self.assets:
            #print(key)
        #-------------------------------

            #-------------------gameloop------------------------

        while True:
            render_scroll = self.logic()
            
            self.display.fill((0, 0, 0, 0))#fill forground with black transparant for mask
            #backgrond img
            self.display_2.blit(self.assets['background'], (0, 0))

            #death check
            manage_death()

            #clouds behind tilemap
            self.clouds.update()
            self.clouds.render(self.display_2, offset=render_scroll)
            self.tilemap.render(self.display_2, offset=render_scroll)

            #mange keys
            manage_keys()

            #enemy calls
            manage_enemies()

            #player calls
            if not self.dead:
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display_2, offset=render_scroll)

            #enemy projectile calls
            manage_enemy_projectiles()

            #spark from projectiles calls
            manage_projectile_sparks()

            #manage sillouette before particles
            manage_mask()
            
            #leaf particles calls
            manage_particles()
                
            #input
            self.keyboard_input()
                
            #manage transition
            manage_transition()

            self.hud.render(self.display)

            

            #display
            self.display_2.blit(self.display, (0, 0))#draw game back on top / "merge displays"
            screenshake_offset = manage_screenshake()
            self.screen.blit(pygame.transform.scale(self.display_2, self.screen.get_size()), screenshake_offset)#render displays
            pygame.display.update()
            self.clock.tick(60)

    def keyboard_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = True
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = True
                if event.key == pygame.K_UP:
                    if self.player.jump():
                        self.sfx['jump'].play(0)
                if event.key == pygame.K_x:
                    if self.player.dash():
                        self.sfx['dash'].play(0)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.movement[0] = False
                if event.key == pygame.K_RIGHT:
                    self.movement[1] = False

Game().run()

#
#
#

def controller_input():
    #d-pad
    if event.type == pygame.JOYHATMOTION:
        hat_x, hat_y = event.value                    
        self.movement[0] = hat_x == -1  # Left → True if pressed
        self.movement[1] = hat_x == 1   # Right → True if pressed
    #buttons
    if event.type == pygame.JOYBUTTONDOWN:
        if event.button == 0:# A button
            self.player.jump()
        if event.button == 2:# X button
            self.player.dash()

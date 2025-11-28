import pygame, math, random
from scripts.particle import Particle
from scripts.spark import Spark
from scripts.projectile import Projectile
from scripts.entities.entities import PhysicsEntity

class Enemy(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)
        self.walking = 0

    def update(self, tilemap, movement=(0, 0)):
        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):#check solid ground
                if self.collisions['right'] or self.collisions['left']:#if run intowall flip
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])#update x movement
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking -1)#decrement walking
            if not self.walking:#shoot
                dis_x = self.game.player.pos[0] - self.pos[0] 
                dis_y = self.game.player.pos[1] - self.pos[1] 
                distance = (dis_x, dis_y)
                if (abs(dis_y) < 16):
                    if (self.flip and dis_x < 0):#looking left and player is to the left
                        self.game.sfx['shoot'].play(0)
                        proj_pos = [self.rect().centerx - 7, self.rect().centery]
                        proj_ani = self.game.assets['enemy/projectile'] 
                        new_proj = Projectile(self.game, proj_pos, (6, 4), -1.5, proj_ani, self.flip) 
                        self.game.projectiles.append(new_proj)
                        #add parks
                        for i in range(4):
                            spark_pos = self.game.projectiles[-1].pos
                            spark_angle = random.random() - 0.5 + math.pi#left
                            spark_speed = 2 + random.random()
                            new_spark = Spark(spark_pos, spark_angle, spark_speed)
                            self.game.sparks.append(new_spark)
                    if (not self.flip and dis_x > 0):#looking right and player is to the right
                        self.game.sfx['shoot'].play(0)
                        proj_pos = [self.rect().centerx + 7, self.rect().centery]
                        proj_ani = self.game.assets['enemy/projectile'] 
                        new_proj = Projectile(self.game, proj_pos, (6, 4), 1.5, proj_ani, self.flip) 
                        self.game.projectiles.append(new_proj)
                        #add parks
                        for i in range(4):
                            spark_pos = self.game.projectiles[-1].pos
                            spark_angle = random.random() - 0.5#right
                            spark_speed = 2 + random.random()
                            new_spark = Spark(spark_pos, spark_angle, spark_speed)
                            self.game.sparks.append(new_spark)
        elif random.random() < 0.01:#ocasionally walk for 30 to 120 secs
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)

        if movement[0] != 0:
            self.set_action('run')
        else:
            self.set_action('idle')

        #killed by dash
        if abs(self.game.player.dashing) >= 50:#if player is dashing
            if self.rect().colliderect(self.game.player.rect()):#and player rect collides
                self.game.sfx['hit'].play(0)
                #screenshake
                self.game.screenshake = max(16, self.game.screenshake)
                for i in range(30):#burst effect of sparks and particles
                    #add sparks
                    spark_pos = self.game.player.rect().center
                    spark_angle = random.random() * math.pi * 2
                    spark_speed = random.random() * 5
                    new_spark = Spark(spark_pos, spark_angle, spark_speed)
                    self.game.sparks.append(new_spark)
                    #add particles
                    pos = self.game.player.rect().center
                    velocity_x = math.cos(spark_angle + math.pi) * spark_speed * 0.5
                    velocity_y = math.sin(spark_angle + math.pi) * spark_speed * 0.5
                    particle_velocity = [velocity_x, velocity_y]
                    new_particle = Particle(self.game, 'particle', pos, velocity=particle_velocity, frame=random.randint(0, 7))
                    self.game.particles.append(new_particle)
                #2 big sparks from sides of enemy
                self.game.sparks.append(Spark(self.rect().center, 0, 5 + random.random()))#left
                self.game.sparks.append(Spark(self.rect().center, math.pi, 5 + random.random()))#right
                #value for kill
                return True

    def render(self, surface, offset=(0, 0)):
        super().render(surface, offset=offset)
        
        #enemy gun blit
        if self.flip:
            flipped_gun = pygame.transform.flip(self.game.assets['gun'], True, False).convert_alpha()
            gun_pos_x = self.rect().centerx - 4 - self.game.assets['gun'].get_width() - offset[0] 
            gun_pos_y = self.rect().centery - offset[1]
            gun_pos = (gun_pos_x, gun_pos_y)
            surface.blit(flipped_gun, gun_pos)
        else:
            gun_pos_x = self.rect().centerx + 4 - offset[0] 
            gun_pos_y = self.rect().centery - offset[1]
            gun_pos = (gun_pos_x, gun_pos_y)
            surface.blit(self.game.assets['gun'], gun_pos)

class Barrel_bomber(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'barrel_bomber', pos, size)
        self.walking = 0
        self.norm_ani_offset = (-4, 0)
        self.flip_ani_offset = (-4, 0)

    def update(self, tilemap, movement=(0, 0)):
        if self.flip:
            self.ani_offset = self.flip_ani_offset
        else:
            self.ani_offset = self.norm_ani_offset

        if self.walking:
            if tilemap.solid_check((self.rect().centerx + (-7 if self.flip else 7), self.pos[1] + 23)):#check solid ground
                if self.collisions['right'] or self.collisions['left']:#if run intowall flip
                    self.flip = not self.flip
                else:
                    movement = (movement[0] - 0.5 if self.flip else 0.5, movement[1])#update x movement
            else:
                self.flip = not self.flip
            self.walking = max(0, self.walking -1)#decrement walking
            
        if random.random() < 0.01:#ocasionally walk for 30 to 120 secs
            self.walking = random.randint(30, 120)

        super().update(tilemap, movement=movement)

        if movement[0] != 0 and self.action != 'attack':
            self.set_action('run')
        else:
            self.set_action('idle')


    def render(self, surface, offset=(0, 0)):
        super().render(surface, offset=offset)
        


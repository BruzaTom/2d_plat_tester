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


class Player(PhysicsEntity):
    def __init__(self, game, pos, size, ani_offset):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
        self.lost_timer = 0
        self.norm_ani_offset = ani_offset[0]
        self.flip_ani_offset = ani_offset[1]

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement=movement)


        #manage ani_offsets according to charcter
        if self.flip:
            self.ani_offset = self.flip_ani_offset
        else:
            self.ani_offset = self.norm_ani_offset

            
        self.air_time += 1

        #check if player is lost
        lost = not (self.collisions['up'] or self.collisions['down'] or self.collisions['right'] or self.collisions['left'])
        if lost:
            self.lost_timer += 1
        else:
            self.lost_timer = 0
        if self.lost_timer > 120:#falling off map
            self.game.dead += 1
            self.game.screenshake = max(16, self.game.screenshake)

        if self.collisions['down']:
            self.air_time = 0
            self.jumps = 1
        
        #conditions for wall_slide
        l_r_collide = (self.collisions['right'] or self.collisions['left'])
        in_air = self.air_time > 4 
        falling = self.velocity[1] > 0 
        #(if hit wall on either side) and (in the air and falling)
        if l_r_collide and (in_air and falling):
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)
            if self.collisions['right']:
                self.flip = False
            else:
                self.flip = True
            self.set_action('wall_slide')
        #else no wall_slide
        else:
            self.wall_slide = False

        if not self.wall_slide:
            if self.dashing > 50 or self.dashing < -50:
                if 'player/dash' in self.game.assets:
                    self.set_action('dash') 
            elif self.velocity[1] > 1:
                if 'player/fall' in self.game.assets:
                    self.set_action('fall')
                else:
                    pass
            elif self.air_time > 4:
                self.set_action('jump')
            elif movement[0] != 0:
                self.set_action('run')
            else:
                self.set_action('idle')

        #dashing
        if abs(self.dashing) in {60, 50}:#burst at beginning and end
            for i in range(20):
                #burst of particles
                angle = random.random() * math.pi * 2#correct way to set an angle
                speed = random.random() * 0.5 + 0.5#generate a speed from 0.5 to 1
                p_velocity = [math.cos(angle) * speed, math.sin(angle) * speed]#trig formula for particle velocity (used alot in games)
                new_particle = Particle(self.game, 'particle', self.rect().center, velocity=p_velocity, frame=random.randint(0, 7))
                self.game.particles.append(new_particle)
        if self.dashing > 0:
            self.dashing = max(0, self.dashing - 1)
        if self.dashing < 0:
            self.dashing = min(0, self.dashing + 1)
        if abs(self.dashing) > 50:
            #divide dashing by 8 negative or positive
            self.velocity[0] = abs(self.dashing) / self.dashing * 8
            #cause sudden stop to dash
            if abs(self.dashing) == 51:#reason for 50 is to act as cool down
                self.velocity[0] *= 0.1
            #trailing particles
            p_velocity = [abs(self.dashing) / self.dashing * random.random() * 3, 0]
            new_particle = Particle(self.game, 'particle', self.rect().center, velocity=p_velocity, frame=random.randint(0, 7))

            self.game.particles.append(new_particle)

        #normalize towards zero from wall jump
        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def render(self, surface, offset=(0, 0)):
        #if player is not dashing just call inherited render 
        super().render(surface, offset=offset)



    def jump(self):
        if self.wall_slide:
            if self.flip and self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                #trigger jump animation
                self.air_time = 5
                #ensure that jumps dosent fall below 0
                self.jumps = max(0, self.jumps - 1)
                #handy return true to hook on some functinality possibly
                return True
            if not self.flip and self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps:
            self.velocity[1] = -3
            self.jumps -= 1
            self.airtime = 5
            return True

    def dash(self):
        if not self.dashing:
            if self.flip:
                self.dashing = -60
            else:
                self.dashing = 60
            return True

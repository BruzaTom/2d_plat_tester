import pygame, math, random
from scripts.particle import Particle
from scripts.entities.entities import PhysicsEntity
from scripts.utils import Animation, load_images

class Samuri(PhysicsEntity):
    def __init__(self, game, pos, health, size=(8, 16)):
        assets = {
                    'player/idle': Animation(load_images(f'entities/samuri/idle'), img_dur=6),
                    'player/run': Animation(load_images(f'entities/samuri/run'), img_dur=4),
                    'player/jump': Animation(load_images(f'entities/samuri/jump'), img_dur=4),
                    'player/slide': Animation(load_images(f'entities/samuri/idle'), img_dur=4),
                    'player/wall_slide': Animation(load_images(f'entities/samuri/wall_slide'), img_dur=8),
                    }
        game.assets.update(assets)
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
        self.lost_timer = 0
        self.norm_ani_offset = (-3, 0)
        self.flip_ani_offset = (-5, 0)
        self.health = health

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

class Player(PhysicsEntity):
    def __init__(self, game, pos, health, size=(8, 16)):
        assets = {
                    'player/idle': Animation(load_images(f'entities/player/idle'), img_dur=6),
                    'player/run': Animation(load_images(f'entities/player/run'), img_dur=4),
                    'player/jump': Animation(load_images(f'entities/player/jump'), img_dur=4),
                    'player/slide': Animation(load_images(f'entities/player/idle'), img_dur=4),
                    'player/wall_slide': Animation(load_images(f'entities/player/wall_slide'), img_dur=8),
                    }
        game.assets.update(assets)
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
        self.lost_timer = 0
        self.norm_ani_offset = (-3, -3)
        self.flip_ani_offset = (-3, -3)
        self.health = health

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

class Samurai2(PhysicsEntity):
    def __init__(self, game, pos, health, size=(10, 25)):
        assets = {
                    'player/idle': Animation(load_images(f'entities/samurai2/idle'), img_dur=6),
                    'player/run': Animation(load_images(f'entities/samurai2/run'), img_dur=4),
                    'player/jump': Animation(load_images(f'entities/samurai2/jump'), img_dur=4),
                    'player/slide': Animation(load_images(f'entities/samurai2/idle'), img_dur=4),
                    'player/wall_slide': Animation(load_images(f'entities/samurai2/wall_slide'), img_dur=8),
                    'player/fall': Animation(load_images(f'entities/samurai2/fall'), img_dur=8),
                    'player/dash': Animation(load_images(f'entities/samurai2/dash'), img_dur=2, loop = False),
                    }
        game.assets.update(assets)
        super().__init__(game, 'player', pos, size)
        self.air_time = 0
        self.jumps = 1
        self.wall_slide = False
        self.dashing = 0
        self.lost_timer = 0
        self.norm_ani_offset = (-36, -26)
        self.flip_ani_offset = (-51, -26)
        self.health = health

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

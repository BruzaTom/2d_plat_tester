import math, pygame

class Spark:
    def __init__(self, pos, angle, speed):
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed

    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)
        #for kill bool
        #if speed has value return false
        #if speed is 0 return true
        return not self.speed

    def render(self, surface, offset=(0, 0)):
        #trigganaomitry for park shape

        #point 1 forward point
        p_one_x = self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0] 
        p_one_y = self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1] 
        #point 2 right or left
        p_two_x = self.pos[0] + math.cos(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[0] 
        p_two_y = self.pos[1] + math.sin(self.angle + math.pi * 0.5) * self.speed * 0.5 - offset[1] 
        #point 3 back point
        p_three_x = self.pos[0] + math.cos(self.angle + math.pi) * self.speed * 3 - offset[0] 
        p_three_y = self.pos[1] + math.sin(self.angle + math.pi) * self.speed * 3 - offset[1] 
        #point 4 right or left
        p_four_x = self.pos[0] + math.cos(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[0] 
        p_four_y = self.pos[1] + math.sin(self.angle - math.pi * 0.5) * self.speed * 0.5 - offset[1] 
        render_points = [
                (p_one_x, p_one_y),
                (p_two_x, p_two_y),
                (p_three_x, p_three_y),
                (p_four_x, p_four_y),
                ]

        pygame.draw.polygon(surface, (255, 255, 255), render_points)

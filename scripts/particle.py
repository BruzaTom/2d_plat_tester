#particals such as leaves falling from a tree
class Particle:
    def __init__(self, game, p_type, pos, velocity=[0, 0], frame=0):
        self.game = game
        self.p_type = p_type
        self.pos = list(pos)
        self.velocity = list(velocity)
        self.animation = self.game.assets['particle/' + p_type].copy()
        self.frame = frame

    def update(self):
        kill = False
        if self.animation.done:
            kill = True

        self.pos[0] += self.velocity[0]
        self.pos[1] += self.velocity[1]

        self.animation.update()

        return kill

    def render(self, surface, offset=(0, 0)):
        img = self.animation.img()
        img_x_os = self.pos[0] - offset[0] - img.get_width() // 2
        img_y_os = self.pos[1] - offset[1] - img.get_height() // 2
        img_os_pos = (img_x_os, img_y_os)
        surface.blit(img, img_os_pos) 


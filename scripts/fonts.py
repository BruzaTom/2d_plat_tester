import pygame, sys

class Font:
    def __init__(self, path):
        self.spacing = 1
        self.char_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';','%'] 
        font_image = pygame.image.load(path).convert_alpha()
        current_char_width = 0
        self.chars = {}
        char_count = 0
        for x in range(font_image.get_width()):
            c = font_image.get_at((x, 0))
            if c[0] == 127:
                clip_x = x - current_char_width
                char_image = self.clip(font_image, clip_x, 0, current_char_width, font_image.get_height())
                self.chars[self.char_order[char_count]] = char_image.copy()
                char_count += 1 
                current_char_width = 0
            else:
                current_char_width += 1
        self.space_width = self.chars['A'].get_width()


    def clip(self, surf, x, y, x_axis, y_axis):
        handle_surf = surf.copy()
        rect = pygame.Rect(x, y, x_axis, y_axis)
        handle_surf.set_clip(rect)
        img = surf.subsurface(handle_surf.get_clip())
        return img.copy()

    def render(self, surf, text, loc):
        x_offset = 0
        for char in text:
            if char != ' ':
                surf.blit(self.chars[char], (loc[0] + x_offset, loc[1]))
                x_offset += self.chars[char].get_width() + self.spacing
            else:
                x_offset += self.space_width + self.spacing

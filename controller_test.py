import pygame
pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No joystick found.")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()
print("Joystick initialized:", joystick.get_name())

screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(60)


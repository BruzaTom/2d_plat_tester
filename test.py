import pygame, sys
from scripts.utils import load_image

pygame.init()
screen = pygame.display.set_mode((400, 300))
clock = pygame.time.Clock()

# Load your axe sprite (transparent background recommended)
axe_img = load_image('entities/barrel_bomber/bomb.png')

# Position and rotation state
x, y = 200, 150
angle = 0
speed_x = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Update position and rotation
    x += speed_x
    angle += 10  # degrees per frame

    # Rotate image
    rotated = pygame.transform.rotate(axe_img, angle)
    rect = rotated.get_rect(center=(x, y))

    # Draw
    screen.fill((30, 30, 30))
    screen.blit(rotated, rect)
    pygame.display.flip()
    clock.tick(60)


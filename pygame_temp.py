# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random

WIDTH = 800
HEIGHT = 400
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Цикл игры
running = True
while running:
    clock.tick(FPS)
    white_keys = 7

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE,
                     ( 80, 10, 80, 80), 0, 5)
    pygame.draw.rect(screen, BLACK,
                     (90, 20, 40, 40), 0, 5)
    pygame.draw.rect(screen, WHITE,
                     (500, 10, 80, 80), 0, 5)
    pygame.draw.rect(screen, BLACK,
                     (530, 40, 40, 40), 0, 5)
    for i in range(white_keys):
        pygame.draw.rect(screen, WHITE,(50 + i * 85, 100, 80, 200), 0, 5)
    pygame.display.flip()

pygame.quit()
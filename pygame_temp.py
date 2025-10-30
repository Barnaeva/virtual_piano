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

sounds = {
    'S': pygame.mixer.Sound("sounds/do.wav"),
    'D': pygame.mixer.Sound("sounds/re.wav"),
    'F': pygame.mixer.Sound("sounds/mi.wav"),
    'G': pygame.mixer.Sound("sounds/fa.wav"),
    'H': pygame.mixer.Sound("sounds/salt.wav"),
    'J': pygame.mixer.Sound("sounds/la.wav"),
    'K': pygame.mixer.Sound("sounds/c.wav"),
    'L': pygame.mixer.Sound("sounds/do2.wav")
}

# Цикл игры
running = True
while running:
    clock.tick(FPS)
    white_keys = 8

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # клавиша A
                sounds['S'].play()
            elif event.key == pygame.K_d:
                sounds['D'].play()
            elif event.key == pygame.K_f:
                sounds['F'].play()
            elif event.key == pygame.K_g:
                sounds['G'].play()
            elif event.key == pygame.K_h:
                sounds['H'].play()
            elif event.key == pygame.K_j:
                sounds['J'].play()
            elif event.key == pygame.K_k:
                sounds['K'].play()
            elif event.key == pygame.K_l:
                sounds['L'].play()
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    for i in range(white_keys):
        pygame.draw.rect(screen, WHITE,(50 + i * 85, 100, 80, 200), 0, 5)
    pygame.display.flip()

pygame.quit()
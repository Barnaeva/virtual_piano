import pygame

WIDTH = 800
HEIGHT = 400
FPS = 30

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мое пианино - Режим: Октава 1")
clock = pygame.time.Clock()

# Разные наборы звуков (режимы)
sound_modes = {
    "1": {
        'S': pygame.mixer.Sound("sounds/grandpiano/do.wav"),
        'D': pygame.mixer.Sound("sounds/grandpiano/re.wav"),
        'F': pygame.mixer.Sound("sounds/grandpiano/mi.wav"),
        'G': pygame.mixer.Sound("sounds/grandpiano/fa.wav"),
        'H': pygame.mixer.Sound("sounds/grandpiano/salt.wav"),
        'J': pygame.mixer.Sound("sounds/grandpiano/la.wav"),
        'K': pygame.mixer.Sound("sounds/grandpiano/si.wav")
    },
    "2": {
        'S': pygame.mixer.Sound("sounds/piano/do.wav"),
        'D': pygame.mixer.Sound("sounds/piano/re.wav"),
        'F': pygame.mixer.Sound("sounds/piano/mi.wav"),
        'G': pygame.mixer.Sound("sounds/piano/fa.wav"),
        'H': pygame.mixer.Sound("sounds/piano/salt.wav"),
        'J': pygame.mixer.Sound("sounds/piano/la.wav"),
        'K': pygame.mixer.Sound("sounds/piano/si.wav")
    }
}

# Текущий режим
current_mode = "1"
current_sounds = sound_modes[current_mode]

# Количество клавиш (может меняться в зависимости от режима)
key_count = 7  # для вашего текущего набора

# Цикл игры
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            # Переключение режимов по клавише TAB
            if event.key == pygame.K_TAB:
                if current_mode == "1":
                    current_mode = "2"
                else:
                    current_mode = "1"

                current_sounds = sound_modes[current_mode]
                pygame.display.set_caption(f"Мое пианино - Режим: {current_mode}")
                print(f"Переключено на: {current_mode}")

            # Воспроизведение нот
            match event.key:
                case pygame.K_s:
                    current_sounds['S'].play()
                case pygame.K_d:
                    current_sounds['D'].play()
                case pygame.K_f:
                    current_sounds['F'].play()
                case pygame.K_g:
                    current_sounds['G'].play()
                case pygame.K_h:
                    current_sounds['H'].play()
                case pygame.K_j:
                    current_sounds['J'].play()
                case pygame.K_k:
                    current_sounds['K'].play()

    # Отрисовка
    screen.fill(BLACK)

    # Рисуем белые клавиши
    for i in range(key_count):
        pygame.draw.rect(screen, WHITE, (50 + i * 85, 100, 80, 200), 0, 5)

    # Отображаем текущий режим на экране
    font = pygame.font.Font(None, 36)
    mode_text = font.render(f"Режим: {current_mode} (TAB для переключения)", True, WHITE)
    screen.blit(mode_text, (50, 50))

    # Подписи клавиш
    key_labels = ['S', 'D', 'F', 'G', 'H', 'J', 'K']
    for i, label in enumerate(key_labels):
        key_text = font.render(label, True, BLACK)
        screen.blit(key_text, (85 + i * 85, 180))

    pygame.display.flip()

pygame.quit()
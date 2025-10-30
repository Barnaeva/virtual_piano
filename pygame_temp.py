import pygame
from Button import ImageButton

WIDTH = 700
HEIGHT = 400
FPS = 30

LIGHT_PINK_2 = (255, 150, 170)
PASTEL_PINK = (255, 209, 220)
LIGHT_PINK = (240, 182, 193)
WHITE = (255, 255, 255)


pygame.init()

pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
pygame.mixer.set_num_channels(16)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Мое пианино - Режим:  1")
clock = pygame.time.Clock()

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
    },
    "3": {
        'S': pygame.mixer.Sound("sounds/bam/do.wav"),
        'D': pygame.mixer.Sound("sounds/bam/re.wav"),
        'F': pygame.mixer.Sound("sounds/bam/mi.wav"),
        'G': pygame.mixer.Sound("sounds/bam/fa.wav"),
        'H': pygame.mixer.Sound("sounds/bam/salt.wav"),
        'J': pygame.mixer.Sound("sounds/bam/la.wav"),
        'K': pygame.mixer.Sound("sounds/bam/si.wav")
    }
}

# Текущий режим
current_mode = "1"
current_sounds = sound_modes[current_mode]

# Количество клавиш
key_count = 7

key_glow_time = [0] * key_count
GLOW_DURATION = 300
mode_button=ImageButton(550,30,100,40,"meow",(240, 182, 193),(255, 150, 170),"sounds/click.wav")
# Цикл игры
running = True
while running:
    clock.tick(FPS)
    current_time = pygame.time.get_ticks()  # текущее время

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif mode_button.handle_event(event):
            current_mode = "2" if current_mode == "1" else "3" if current_mode == "2" else "1"
            current_sounds = sound_modes[current_mode]
            pygame.display.set_caption(f"Мое пианино - Режим: {current_mode}")
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_TAB:
                    current_mode = "2" if current_mode == "1" else "3" if current_mode == "2" else "1"
                    current_sounds = sound_modes[current_mode]
                    pygame.display.set_caption(f"Мое пианино - Режим: {current_mode}")

                case pygame.K_s:
                    current_sounds['S'].play()
                    key_glow_time[0] = current_time
                case pygame.K_d:
                    current_sounds['D'].play()
                    key_glow_time[1] = current_time
                case pygame.K_f:
                    current_sounds['F'].play()
                    key_glow_time[2] = current_time
                case pygame.K_g:
                    current_sounds['G'].play()
                    key_glow_time[3] = current_time
                case pygame.K_h:
                    current_sounds['H'].play()
                    key_glow_time[4] = current_time
                case pygame.K_j:
                    current_sounds['J'].play()
                    key_glow_time[5] = current_time
                case pygame.K_k:
                    current_sounds['K'].play()
                    key_glow_time[6] = current_time
        mode_button.handle_event(event)

    # Отрисовка
    screen.fill(LIGHT_PINK)

    mode_button.check_hover(pygame.mouse.get_pos())
    mode_button.draw(screen)

    for i in range(key_count):
        # Проверяем, нужно ли подсвечивать клавишу
        if key_glow_time[i] > 0 and (current_time - key_glow_time[i]) < GLOW_DURATION:
            color = PASTEL_PINK
        else:
            color = WHITE  # обычная клавиша
            if key_glow_time[i] > 0:
                key_glow_time[i] = 0  # сбрасываем таймер

        pygame.draw.rect(screen, color, (50 + i * 85, 100, 80, 200), 0, 5)

    font = pygame.font.Font(None, 36)
    mode_text = font.render(f"Режим: {current_mode} (TAB для переключения)", True, WHITE)
    screen.blit(mode_text, (50, 50))

    key_labels = ['S', 'D', 'F', 'G', 'H', 'J', 'K']
    for i, label in enumerate(key_labels):
        key_text = font.render(label, True, LIGHT_PINK_2)
        screen.blit(key_text, (85 + i * 85, 180))

    pygame.display.flip()

pygame.quit()
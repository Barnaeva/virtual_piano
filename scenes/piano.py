import pygame
from config import *
from ui.buttons import ImageButton


class PianoScene:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.sound_modes = self.load_sounds()
        self.current_mode = "1"
        self.current_sounds = self.sound_modes[self.current_mode]
        self.key_glow_time = [0] * KEY_COUNT

        self.mode_button = ImageButton(
            MODE_BUTTON_X, MODE_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, "РЕЖИМ ЗВУКА",
            BACKGROUND, BUTTON, BUTTON_SOUND_PATH
        )
        self.exit_button = ImageButton(
            EXIT_BUTTON_X, EXIT_BUTTON_Y, EXIT_BUTTON_WIDTH, EXIT_BUTTON_HEIGHT, "ВЫХОД",
            BACKGROUND, BUTTON,BUTTON_SOUND_PATH
        )
        self.mode_button_game = ImageButton(
            MODE_GAME_BUTTON_X, MODE_GAME_BUTTON_Y, BUTTON_WIDTH, BUTTON_HEIGHT, "РЕЖИМ ИГРЫ",
            BACKGROUND, BUTTON, BUTTON_SOUND_PATH
        )
        self.need_switch_to_game = False

    def load_sounds(self):
        sound_modes = {}
        for mode_name, sound_paths in SOUND_PATHS.items():
            sound_modes[mode_name] = {}
            for note, path in sound_paths.items():
                try:
                    sound_modes[mode_name][note] = pygame.mixer.Sound(path)
                except pygame.error as e:
                    print(f"Ошибка загрузки звука {path}: {e}")
                    sound_modes[mode_name][note] = None
        return sound_modes

    def switch_mode(self):
        self.current_mode = "2" if self.current_mode == "1" else "3" if self.current_mode == "2" else "1"
        self.current_sounds = self.sound_modes[self.current_mode]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.mode_button.handle_event(event):
                self.switch_mode()

            if self.exit_button.handle_event(event):
                pygame.time.delay(130)
                return False

            if self.mode_button_game.handle_event(event):
                self.need_switch_to_game = True


            elif event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_s:
                        self.current_sounds['S'].play()
                        self.key_glow_time[0] = pygame.time.get_ticks()
                    case pygame.K_d:
                        self.current_sounds['D'].play()
                        self.key_glow_time[1] = pygame.time.get_ticks()
                    case pygame.K_f:
                        self.current_sounds['F'].play()
                        self.key_glow_time[2] = pygame.time.get_ticks()
                    case pygame.K_g:
                        self.current_sounds['G'].play()
                        self.key_glow_time[3] = pygame.time.get_ticks()
                    case pygame.K_h:
                        self.current_sounds['H'].play()
                        self.key_glow_time[4] = pygame.time.get_ticks()
                    case pygame.K_j:
                        self.current_sounds['J'].play()
                        self.key_glow_time[5] = pygame.time.get_ticks()
                    case pygame.K_k:
                        self.current_sounds['K'].play()
                        self.key_glow_time[6] = pygame.time.get_ticks()

        return True

    def update(self):
        current_time = pygame.time.get_ticks()

        for i in range(KEY_COUNT):
            if self.key_glow_time[i] > 0 and current_time - self.key_glow_time[i] > GLOW_DURATION:
                self.key_glow_time[i] = 0

        self.mode_button.check_hover(pygame.mouse.get_pos())
        self.exit_button.check_hover(pygame.mouse.get_pos())
        self.mode_button_game.check_hover(pygame.mouse.get_pos())

    def draw(self):
        self.screen.fill(BACKGROUND)

        for i in range(KEY_COUNT):
            x = PIANO_START_X + i * (KEY_WIDTH + KEY_SPACING)

            if (self.key_glow_time[i] > 0 and
                    (pygame.time.get_ticks() - self.key_glow_time[i]) < GLOW_DURATION):
                color = KEYS_PIANO
            else:
                color = TEXT

            pygame.draw.rect(self.screen, color,
                             (x, PIANO_START_Y, KEY_WIDTH, KEY_HEIGHT), 0, 5)

        self.mode_button.draw(self.screen)
        self.exit_button.draw(self.screen)
        self.mode_button_game.draw(self.screen)

        font = pygame.font.SysFont(FONT, SIZE_TEXT)

        mode_name = CURRENT_MODE.get(self.current_mode, f"Режим {self.current_mode}")
        mode_text = font.render(f"Режим: {mode_name} ", True, TEXT)

        self.screen.blit(mode_text, (MODE_TEXT_X, MODE_TEXT_Y))

        for i, label in enumerate(KEY_LABELS):
            key_x = PIANO_START_X + i * (KEY_WIDTH + KEY_SPACING) + KEY_TEXT_OFFSET_X
            key_y = PIANO_START_Y + KEY_TEXT_OFFSET_Y

            key_text = font.render(label, True, BUTTON)
            self.screen.blit(key_text, (key_x, key_y))


    def run(self):
        self.clock.tick(FPS)

        if not self.handle_events():
            return False

        self.update()
        self.draw()
        pygame.display.flip()

        return True
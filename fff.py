# test_falling.py
import pygame
import sys
import os

sys.path.append(os.path.dirname(__file__))

from config import *
from ui.buttons import ImageButton


class FallingNotesTest:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.sound_modes = self.load_sounds()
        self.current_sounds = self.sound_modes["1"]

        self.key_glow_time = [0] * KEY_COUNT

        self.falling_notes = []
        self.fall_speed = 5

        # Мелодия "Гуси"
        self.test_melody = ['G', 'F', 'D', 'S', 'H', 'H',
                            'G', 'F', 'D', 'S', 'H', 'H',
                            'G', 'J', 'J', 'G', 'F', 'H', 'H', 'F',
                            'D','F','G','D','S','S',
                            'G', 'J', 'J', 'G',
                            'F', 'H', 'H', 'F',
                            'D','F','G','D','S','S']
        self.test_melody_JINGLEBELLS = ['F', 'F', 'F', 'F', 'F', 'F',
                            'F', 'H', 'S', 'D', 'F',
                            'G', 'G', 'G', 'G', 'F', 'F', 'F', 'F',
                            'D', 'D', 'F', 'D', 'H']
        '''Гуси.
4 3 2 1 5 5
Жи-ли у ба-бу-си
4 3 2 1 5 5
Два ве-се-лых гу-ся
4 6 6 4 3 5 5 3
О-дин се-рый, дру-гой бе-лый,
2 3 4 2 1 1
Два ве-се-лых гу-ся!
4 6 6 4 3 5 5 3
О-дин се-рый, дру-гой бе-лый,
2 3 4 2 1 1
Два ве-се-лых гу-ся!'''

        self.next_note_time = 0
        self.note_interval = 800
        self.current_melody_index = 0

        self.key_top = 100  # Верх клавиши
        self.key_bottom = 300  # Низ клавиши

        # Кнопки
        self.quit_button = ImageButton(50, 30, 120, 40, "ВЫХОД",
                                       BACKGROUND, BUTTON, "sounds/click.wav")

    def load_sounds(self):
        sound_modes = {}
        for mode_name, sound_paths in SOUND_PATHS.items():
            sound_modes[mode_name] = {}
            for note, path in sound_paths.items():
                try:
                    sound_modes[mode_name][note] = pygame.mixer.Sound(path)
                except:
                    sound_modes[mode_name][note] = None
        return sound_modes

    def add_falling_note(self, note_name):
        """Добавляет падающую ноту"""
        note_index = KEY_LABELS.index(note_name)

        note = {
            'note_index': note_index,
            'note_name': note_name,
            'x': 50 + note_index * 85,
            'y': -50,
            'width': 70,
            'height': 30,
            'color': BUTTON,
            'active': True
        }
        self.falling_notes.append(note)

    def update_falling_notes(self):
        """Обновляет падающие ноты"""
        current_time = pygame.time.get_ticks()

        # Добавляем новые ноты по таймеру
        if current_time > self.next_note_time and self.current_melody_index < len(self.test_melody):
            note_to_add = self.test_melody[self.current_melody_index]
            self.add_falling_note(note_to_add)
            self.current_melody_index += 1
            self.next_note_time = current_time + self.note_interval

        # Двигаем ноты вниз
        for note in self.falling_notes[:]:
            note['y'] += self.fall_speed

            # Проверяем попадание (когда центр ноты внутри клавиши)
            note_center_y = note['y'] + note['height'] // 2
            if self.key_top <= note_center_y <= self.key_bottom and note['active']:
                # Если нажата правильная клавиша
                if self.key_glow_time[note['note_index']] > 0:
                    self.falling_notes.remove(note)
                    self.current_sounds[note['note_name']].play()

            # Удаляем упавшие за экран
            if note['y'] > HEIGHT:
                self.falling_notes.remove(note)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if self.quit_button.handle_event(event):
                return False


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

    def draw(self):
        self.screen.fill(BACKGROUND)

        for i in range(KEY_COUNT):
            current_time = pygame.time.get_ticks()
            if self.key_glow_time[i] > 0 and current_time - self.key_glow_time[i] < GLOW_DURATION:
                color = KEYS_PIANO  # Подсветка при нажатии
            else:
                color = TEXT

            pygame.draw.rect(self.screen, color, (50 + i * 85, 100, 80, 200), 0, 5)

        # Падающие ноты
        for note in self.falling_notes:
            pygame.draw.rect(self.screen, note['color'],
                             (note['x'], note['y'], note['width'], note['height']), 0, 5)

            font = pygame.font.Font(None, 24)
            text = font.render(note['note_name'], True, TEXT)
            text_rect = text.get_rect(center=(note['x'] + note['width'] // 2,
                                              note['y'] + note['height'] // 2))
            self.screen.blit(text, text_rect)

        self.quit_button.draw(self.screen)

        font = pygame.font.Font(None, 36)
        instruction = font.render("Нажимайте клавиши когда ноты касаются клавиш!", True, TEXT)
        self.screen.blit(instruction, (50, 350))

        for i, label in enumerate(KEY_LABELS):
            key_text = font.render(label, True, BUTTON)
            self.screen.blit(key_text, (85 + i * 85, 180))

        # Прогресс мелодии
        progress_text = font.render(f"Нота: {self.current_melody_index}/{len(self.test_melody)}", True, TEXT)
        self.screen.blit(progress_text, (600, 30))

    def update(self):
        current_time = pygame.time.get_ticks()

        # Сбрасываем подсветку клавиш
        for i in range(KEY_COUNT):
            if self.key_glow_time[i] > 0 and current_time - self.key_glow_time[i] > GLOW_DURATION:
                self.key_glow_time[i] = 0

        # Обновляем падающие ноты
        self.update_falling_notes()

        # Обновляем кнопку
        mouse_pos = pygame.mouse.get_pos()
        self.quit_button.check_hover(mouse_pos)

    def run(self):
        self.clock.tick(FPS)

        if not self.handle_events():
            return False

        self.update()
        self.draw()
        pygame.display.flip()

        return True


# ЗАПУСК
def main():
    pygame.init()
    pygame.mixer.init(**SOUND_SETTINGS)
    pygame.mixer.set_num_channels(NUM_CHANNELS)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("ТЕСТ: Падающие ноты - Мелодия 'Гуси'")
    clock = pygame.time.Clock()

    test = FallingNotesTest(screen, clock)

    running = True
    while running:
        running = test.run()

    pygame.quit()


if __name__ == "__main__":
    main()
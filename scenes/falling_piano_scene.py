import pygame
from config import *
from scenes.piano import PianoScene
from ui.buttons import ImageButton


class FallingPianoScene(PianoScene):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)



        self.falling_notes = []
        self.fall_speed = 5
        self.is_playing = False


        self.test_melody = ['G', 'F', 'D', 'S', 'H', 'H',
                            'G', 'F', 'D', 'S', 'H', 'H',
                            'G', 'J', 'J', 'G', 'F', 'H', 'H', 'F',
                            'D', 'F', 'G', 'D', 'S', 'S',
                            'G', 'J', 'J', 'G',
                            'F', 'H', 'H', 'F',
                            'D', 'F', 'G', 'D', 'S', 'S']

        self.current_melody_index = 0
        self.next_note_time = 0
        self.note_interval = 800


        self.hit_zone_top = PIANO_START_Y
        self.hit_zone_bottom = PIANO_START_Y + KEY_HEIGHT


        self.start_button = ImageButton(
            MODE_BUTTON_X, HEIGHT*0.27, GAME_BUTTON_WIDTH, GAME_BUTTON_HEIGHT,
            "НАЧАТЬ" if not self.is_playing else "ПАУЗА",
            BACKGROUND, BUTTON, BUTTON_SOUND_PATH
        )

        self.reset_button = ImageButton(
            MODE_BUTTON_X + 10+ GAME_BUTTON_WIDTH , HEIGHT*0.27, GAME_BUTTON_WIDTH, GAME_BUTTON_HEIGHT, "СБРОС",
            BACKGROUND, BUTTON, BUTTON_SOUND_PATH
        )

        self.score = 0
        self.misses = 0

    def add_falling_note(self, note_name):
        if note_name not in KEY_LABELS:
            return

        note_index = KEY_LABELS.index(note_name)

        note = {
            'note_index': note_index,
            'note_name': note_name,
            'x': PIANO_START_X + note_index * (KEY_WIDTH + KEY_SPACING),
            'y': 200,
            'width': KEY_WIDTH,
            'height': 50,
            'color': BUTTON,
            'active': True,
            'hit': False
        }
        self.falling_notes.append(note)

    def update_falling_notes(self):
        """Обновляет падающие ноты"""
        if not self.is_playing:
            return

        current_time = pygame.time.get_ticks()


        if (current_time > self.next_note_time and
                self.current_melody_index < len(self.test_melody)):
            self.add_falling_note(self.test_melody[self.current_melody_index])
            self.current_melody_index += 1
            self.next_note_time = current_time + self.note_interval


        for note in self.falling_notes[:]:
            note['y'] += self.fall_speed

            note_center_y = note['y'] + note['height'] // 2


            if self.hit_zone_top <= note_center_y <= self.hit_zone_bottom:
                if self.key_glow_time[note['note_index']] > 0:

                    note['hit'] = True
                    note['color'] = (0, 255, 0)
                    self.score += 100
                    self.falling_notes.remove(note)



            if note['y'] > HEIGHT:
                self.falling_notes.remove(note)

    def reset_game(self):
        """Сбрасывает игру"""
        self.falling_notes.clear()
        self.current_melody_index = 0
        self.next_note_time = 0
        self.score = 0
        self.misses = 0
        self.is_playing = False
        self.start_button.text = "НАЧАТЬ"

    def handle_events(self):
        events = pygame.event.get()

        for event in events:

            if self.start_button.handle_event(event):
                self.is_playing = not self.is_playing
                self.start_button.text = "ПАУЗА" if self.is_playing else "ПРОДОЛЖИТЬ"
                if self.is_playing and self.current_melody_index == 0:
                    self.next_note_time = pygame.time.get_ticks()
                continue
            elif self.reset_button.handle_event(event):
                self.reset_game()
                continue

        for event in events:
            pygame.event.post(event)

        return super().handle_events()

    def update(self):
        super().update()

        self.update_falling_notes()

        mouse_pos = pygame.mouse.get_pos()
        self.start_button.check_hover(mouse_pos)
        self.reset_button.check_hover(mouse_pos)

    def draw_additional(self):
        pygame.draw.rect(self.screen, (170, 200, 170),
                         (PIANO_START_X , 210,  # x, y
                          KEY_COUNT * (KEY_WIDTH + KEY_SPACING)-5 ,
                          310))

        zone_rect = pygame.Rect(
            PIANO_START_X,
            self.hit_zone_top,
            KEY_COUNT * (KEY_WIDTH + KEY_SPACING) -5,
            self.hit_zone_bottom - self.hit_zone_top
        )

        s = pygame.Surface(zone_rect.size, pygame.SRCALPHA)
        s.fill((170, 200, 170, 100))
        self.screen.blit(s, zone_rect.topleft)
        pygame.draw.rect(self.screen, (170, 200, 170), zone_rect, 2)

        for note in self.falling_notes:
            pygame.draw.rect(self.screen, note['color'],
                             (note['x'], note['y'], note['width'], note['height']), 0, 5)

            font = pygame.font.Font(None, 24)
            text = font.render(note['note_name'], True, TEXT)
            text_rect = text.get_rect(
                center=(note['x'] + note['width'] // 2,
                        note['y'] + note['height'] // 2)
            )
            self.screen.blit(text, text_rect)

        self.start_button.draw(self.screen)
        self.reset_button.draw(self.screen)

        font = pygame.font.SysFont(FONT, SIZE_TEXT)
        if self.is_playing or self.score > 0 or self.misses > 0:
            score_text = font.render(f"Счёт: {self.score}", True, (0, 255, 0))
            progress_text = font.render(
                f"Прогресс: {self.current_melody_index}/{len(self.test_melody)}",
                True, TEXT
            )

            self.screen.blit(score_text, (MODE_TEXT_X, 70))
            self.screen.blit(progress_text, (MODE_TEXT_X, 100))

        instruction = font.render("Нажимайте клавиши когда ноты в красной зоне!", True, TEXT)
        self.screen.blit(instruction, (PIANO_START_X , HEIGHT-70))

    def draw(self):
        super().draw()

        self.draw_additional()
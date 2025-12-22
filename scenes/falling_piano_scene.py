from config import *
from scenes.piano import PianoScene
from ui.buttons import ImageButton
from ui.io_operation import *


class FallingPianoScene(PianoScene):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)

        self.play_icon = load_icon("play.png")
        self.stop_icon = load_icon("stop.png")

        self.falling_notes = []
        self.fall_speed = FALLING_SPEED
        self.is_playing = False

        # Загружаем ВСЕ мелодии

        self.all_melodies = read_json('melodies/mel.json')  # Теперь это список!

        # Текущий индекс мелодии
        self.current_melody_index = 0
        # Текущая мелодия
        self.current_melody_data = self.all_melodies[self.current_melody_index]
        self.current_note_index = 0
        self.melody_start_time = 0
        self.next_note_time = 0

        self.hit_zone_top = PIANO_START_Y
        self.hit_zone_bottom = PIANO_START_Y + KEY_HEIGHT

        # Кнопка старт/пауза
        self.start_button = ImageButton(
            x=PIANO_START_X,
            y=GAME_BUTTON_Y,
            width=START_BUTTON_WIDTH,
            height=GAME_BUTTON_HEIGHT,
            text=None, color=BACKGROUND, hover_color=BUTTON,
            sound_path=BUTTON_SOUND_PATH,
            icon=self.play_icon,
            icon_size=(50, 50)
        )

        # Кнопка сброса
        self.reset_button = ImageButton(
            x=PIANO_START_X + START_BUTTON_WIDTH + GAME_BUTTON_SPACING,
            y=GAME_BUTTON_Y,
            width=GAME_BUTTON_WIDTH,
            height=GAME_BUTTON_HEIGHT,
            text="СБРОС", color=BACKGROUND, hover_color=BUTTON,
            sound_path=BUTTON_SOUND_PATH
        )

        # Кнопка переключения мелодии (текст будет обновляться)
        self.mel_button = ImageButton(
            x=PIANO_START_X + START_BUTTON_WIDTH+GAME_BUTTON_WIDTH + GAME_BUTTON_SPACING * 2,
            y=GAME_BUTTON_Y,
            width=GAME_BUTTON_WIDTH,
            height=GAME_BUTTON_HEIGHT,
            text=self.current_melody_data['name'],  # Название текущей мелодии
            color=BACKGROUND,
            hover_color=BUTTON,
            sound_path=BUTTON_SOUND_PATH
        )

        # Статистика
        self.score = 0
        self.misses = 0
        self.pause_start_time = 0

    def switch_melody(self):
        """Переключает на следующую мелодию по кругу"""
        # Увеличиваем индекс
        self.current_melody_index = (self.current_melody_index + 1) % len(self.all_melodies)

        # Обновляем текущую мелодию
        self.current_melody_data = self.all_melodies[self.current_melody_index]

        # Обновляем текст на кнопке
        self.mel_button.text = self.current_melody_data['name']

        # Если игра была запущена, сбрасываем
        if self.is_playing:
            self.reset_game()

    def reset_game(self):
        """Сбрасывает игру с учетом текущей мелодии"""
        self.falling_notes.clear()
        self.current_note_index = 0
        self.melody_start_time = 0
        self.next_note_time = 0
        self.pause_start_time = 0
        self.score = 0
        self.misses = 0
        self.is_playing = False

        if self.play_icon:
            self.start_button.set_icon(self.play_icon, (50, 50))

    def add_falling_note(self, note_name):
        """Добавляет падающую ноту"""
        if note_name not in KEY_LABELS:
            return

        note_index = KEY_LABELS.index(note_name)

        note = {
            'note_index': note_index,
            'note_name': note_name,
            'x': PIANO_START_X + note_index * (KEY_WIDTH + KEY_SPACING),
            'y': FALLING_NOTES_START_Y,
            'width': KEY_WIDTH,
            'height': FALLING_NOTE_HEIGHT,
            'color': FALLING_NOTE_COLOR,
            'active': True,
            'hit': False
        }
        self.falling_notes.append(note)

    def update_falling_notes(self):
        """Обновляет падающие ноты с учетом относительного времени"""
        if not self.is_playing:
            return

        current_time = pygame.time.get_ticks()

        # Устанавливаем время старта при первом запуске
        if self.current_note_index == 0 and self.melody_start_time == 0:
            self.melody_start_time = current_time
            self.next_note_time = current_time

        # Проверяем, не пришло ли время для следующей ноты
        while (self.current_note_index < len(self.current_melody_data['notes']) and
               current_time >= self.next_note_time):

            note_data = self.current_melody_data['notes'][self.current_note_index]
            self.add_falling_note(note_data['note'])

            # Обновляем время для следующей ноты
            if self.current_note_index + 1 < len(self.current_melody_data['notes']):
                next_delay = self.current_melody_data['notes'][self.current_note_index + 1]['delay']
                self.next_note_time += next_delay

            self.current_note_index += 1

        # Двигаем существующие ноты вниз
        for note in self.falling_notes[:]:
            note['y'] += self.fall_speed

            note_center_y = note['y'] + note['height'] // 2

            # Проверка попадания
            if self.hit_zone_top <= note_center_y <= self.hit_zone_bottom:
                if self.key_glow_time[note['note_index']] > 0:
                    # Попадание!
                    note['hit'] = True
                    note['color'] = FALLING_NOTE_HIT_COLOR
                    self.score += SCORE_PER_HIT
                    self.falling_notes.remove(note)

            # Удаляем упавшие
            if note['y'] > HEIGHT:
                self.falling_notes.remove(note)
                self.misses += 1

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if self.start_button.handle_event(event):
                if not self.is_playing:
                    # ЗАПУСК/ПРОДОЛЖЕНИЕ игры
                    self.is_playing = True

                    if self.stop_icon:
                        self.start_button.set_icon(self.stop_icon, (50, 50))

                    # При старте сбрасываем таймеры
                    if self.current_note_index == 0:
                        self.melody_start_time = pygame.time.get_ticks()
                        self.next_note_time = self.melody_start_time
                    else:
                        # Продолжение после паузы
                        if self.pause_start_time > 0:
                            pause_duration = pygame.time.get_ticks() - self.pause_start_time
                            self.next_note_time += pause_duration
                            self.pause_start_time = 0
                else:
                    # ПАУЗА
                    self.is_playing = False
                    self.pause_start_time = pygame.time.get_ticks()  # ЗАПОМИНАЕМ ВРЕМЯ ПАУЗЫ!

                    if self.play_icon:
                        self.start_button.set_icon(self.play_icon, (50, 50))
                continue

            elif self.reset_button.handle_event(event):
                self.reset_game()
                continue

            elif self.mel_button.handle_event(event):
                self.switch_melody()
                continue

        for event in events:
            pygame.event.post(event)

        return super().handle_events()

    def update(self):
        super().update()
        self.update_falling_notes()

        # Обновляем состояние кнопок
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.check_hover(mouse_pos)
        self.reset_button.check_hover(mouse_pos)
        self.mel_button.check_hover(mouse_pos)

    def draw_additional(self):
        # Рисуем область для падающих нот
        pygame.draw.rect(self.screen, NOTES_AREA_COLOR,
                         (PIANO_START_X, NOTES_AREA_START_Y,
                          KEY_COUNT * (KEY_WIDTH + KEY_SPACING) - 5,
                          NOTES_AREA_HEIGHT))

        # Разделительные линии между нотами
        for i in range(KEY_COUNT):
            x = (PIANO_START_X - KEY_SPACING) + i * (KEY_WIDTH + KEY_SPACING)
            pygame.draw.rect(self.screen, BACKGROUND,
                             (x, NOTES_AREA_START_Y, KEY_SPACING, NOTES_AREA_HEIGHT), 0)

        # Зона попадания
        zone_rect = pygame.Rect(
            PIANO_START_X,
            self.hit_zone_top,
            KEY_COUNT * (KEY_WIDTH + KEY_SPACING) - 5,
            self.hit_zone_bottom - self.hit_zone_top
        )

        # Полупрозрачная зона попадания
        s = pygame.Surface(zone_rect.size, pygame.SRCALPHA)
        s.fill((*HIT_ZONE_COLOR, HIT_ZONE_ALPHA))
        self.screen.blit(s, zone_rect.topleft)
        pygame.draw.rect(self.screen, HIT_ZONE_BORDER_COLOR, zone_rect, 2)

        # Рисуем падающие ноты
        for note in self.falling_notes:
            pygame.draw.rect(self.screen, note['color'],
                             (note['x'], note['y'], note['width'], note['height']), 0, 5)

            font = pygame.font.Font(None, FALLING_NOTE_FONT_SIZE)
            text = font.render(note['note_name'], True, FALLING_NOTE_TEXT_COLOR)
            text_rect = text.get_rect(
                center=(note['x'] + note['width'] // 2,
                        note['y'] + note['height'] // 2)
            )
            self.screen.blit(text, text_rect)

        # Рисуем кнопки
        self.start_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        self.mel_button.draw(self.screen)

        # Статистика и информация
        font = pygame.font.SysFont(FONT, SIZE_TEXT)


        score_text = font.render(f"Счёт: {self.score}", True, SCORE_COLOR)
        misses_text = font.render(f"Промахи: {self.misses}", True, MISSES_COLOR)

        # Прогресс: текущая нота / всего нот В ТЕКУЩЕЙ МЕЛОДИИ
        total_notes = len(self.current_melody_data['notes'])
        progress_text = font.render(
            f"Прогресс: {self.current_note_index}/{total_notes}",
            True, TEXT
        )

        self.screen.blit(score_text, (TEXT_OFFSET_X + 160, TEXT_OFFSET_Y))
        self.screen.blit(misses_text, (TEXT_OFFSET_X + 280 , TEXT_OFFSET_Y))
        self.screen.blit(progress_text, (TEXT_OFFSET_X, TEXT_OFFSET_Y))

        # Инструкция
        instruction = font.render(INSTRUCTION_TEXT, True, TEXT)
        self.screen.blit(instruction, (PIANO_START_X, INSTRUCTION_POS_Y))

        self.draw_mode_game()

    def draw_mode_game(self):
        font = pygame.font.SysFont(FONT, SIZE_TEXT)
        mode_text = font.render(CURRENT_MODE_GAME[1], True, TEXT)
        self.screen.blit(mode_text, (MODE_TEXT_X, MODE_TEXT_Y + 35))

    def draw(self):
        super().draw()
        self.draw_additional()
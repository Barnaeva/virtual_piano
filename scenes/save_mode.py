import wave
import numpy as np
from datetime import datetime
from utils.config import *
from scenes.piano import PianoScene
from utils.buttons import ImageButton
from utils.io_operation import *


class MelodyRecorderScene(PianoScene):
    def __init__(self, screen, clock):
        super().__init__(screen, clock)

        self.all_melodies = read_json('melodies/mel.json')
        self.current_melody_index = 0
        self.list_scroll_offset = 0

        if self.all_melodies:
            self.current_melody_data = self.all_melodies[self.current_melody_index]
        else:
            self.current_melody_data = {'name': 'Нет мелодий', 'flag': 0, 'notes': []}

        self.recording = False
        self.record_start_time = 0
        self.recorded_notes = []
        self.record_button.text = "ВЕРНУТЬСЯ"
        os.makedirs("melodies", exist_ok=True)

        # Переменные для воспроизведения
        self.playing = False
        self.playback_index = 0
        self.playback_start_time = 0
        self.current_playback_notes = []
        self.playback_note_start_time = 0

        self.up_button = ImageButton(
            x=MELODY_LIST_X + MELODY_LIST_WIDTH - 40,
            y=MELODY_LIST_Y,
            width=35,
            height=35,
            text="↑",
            color=BUTTON,
            hover_color=KEYS_PIANO,
            sound_path=BUTTON_SOUND_PATH
        )

        self.down_button = ImageButton(
            x=MELODY_LIST_X + MELODY_LIST_WIDTH - 40,
            y=MELODY_LIST_Y + MELODY_LIST_HEIGHT - 35,
            width=35,
            height=35,
            text="↓",
            color=BUTTON,
            hover_color=KEYS_PIANO,
            sound_path=BUTTON_SOUND_PATH
        )

        self.record_control_button = ImageButton(
            x=RECORD_BUTTON_X-BUTTON_WIDTH-KEY_SPACING, y=PIANO_START_Y-50,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            text="НАЧАТЬ ЗАПИСЬ",
            color=BUTTON, hover_color=KEYS_PIANO,
            sound_path=BUTTON_SOUND_PATH
        )

        self.save_button = ImageButton(
            x=RECORD_BUTTON_X, y=PIANO_START_Y-50,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            text="СОХРАНИТЬ",
            color=BUTTON, hover_color=KEYS_PIANO,
            sound_path=BUTTON_SOUND_PATH
        )

        self.convert_wav_button = ImageButton(
            x=RECORD_BUTTON_X, y=RECORD_BUTTON_Y + (BUTTON_HEIGHT + KEY_SPACING) * 4,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            text="СОХРАНИТЬ .WAV",
            color=BUTTON, hover_color=KEYS_PIANO,
            sound_path=BUTTON_SOUND_PATH
        )

        self.play_button = ImageButton(
            x=RECORD_BUTTON_X, y=RECORD_BUTTON_Y + (BUTTON_HEIGHT + KEY_SPACING) * 5,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            text="ВОСПРОИЗВЕСТИ",
            color=BUTTON, hover_color=KEYS_PIANO,
            sound_path=BUTTON_SOUND_PATH
        )

        self.del_button = ImageButton(
            x=RECORD_BUTTON_X, y=RECORD_BUTTON_Y + (BUTTON_HEIGHT + KEY_SPACING) * 6,
            width=BUTTON_WIDTH, height=BUTTON_HEIGHT,
            text="УДАЛИТЬ",
            color=(180, 60, 60), hover_color=(220, 80, 80),
            sound_path=BUTTON_SOUND_PATH
        )

        self.control_buttons = [
            self.record_control_button,
            self.save_button,
            self.convert_wav_button,
            self.play_button,
            self.del_button,
        ]

        self.need_switch_to_normal = False
        self.last_note_time = 0

    def convert_json_to_wav(self, melody_data=None, filename=None):
        if melody_data is None:
            melody_data = self.current_melody_data

        if not melody_data.get('notes'):
            return False

        try:
            os.makedirs("melodies", exist_ok=True)

            if filename is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"melodies/{melody_data['name']}_{timestamp}.wav"

            sample_rate = 44100
            channels = 1

            current_time = 0
            max_duration = 0
            for note in melody_data['notes']:
                current_time += note['delay']
                max_duration = max(max_duration, current_time + 2000)

            total_duration = max_duration + 1000
            total_samples = int(sample_rate * total_duration / 1000)

            audio_buffer = np.zeros(total_samples, dtype=np.float32)

            current_time = 0
            for note_info in melody_data['notes']:
                current_time += note_info['delay']
                note_name = note_info['note']

                if note_name in self.current_sounds and self.current_sounds[note_name]:
                    sound = self.current_sounds[note_name]

                    sound_array = pygame.sndarray.array(sound)

                    if len(sound_array.shape) == 2:
                        sound_array = sound_array.mean(axis=1)

                    sound_float = sound_array.astype(np.float32) / 32768.0

                    start_sample = int(current_time * sample_rate / 1000)
                    end_sample = min(start_sample + len(sound_float), total_samples)

                    if start_sample < total_samples:
                        length = end_sample - start_sample
                        audio_buffer[start_sample:end_sample] += sound_float[:length]

            max_val = np.max(np.abs(audio_buffer))
            if max_val > 0:
                audio_buffer = audio_buffer / max_val

            audio_int16 = (audio_buffer * 32767).astype(np.int16)

            with wave.open(filename, 'w') as wav_file:
                wav_file.setnchannels(channels)
                wav_file.setsampwidth(2)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio_int16.tobytes())

            return True

        except Exception as e:
            print(f"✗ Ошибка: {e}")
            import traceback
            traceback.print_exc()
            return False

    def scroll_list(self, direction):
        if direction == "up" and self.list_scroll_offset > 0:
            self.list_scroll_offset -= 1
        elif direction == "down":
            max_offset = max(0, len(self.all_melodies) - MAX_VISIBLE_MELODIES)
            if self.list_scroll_offset < max_offset:
                self.list_scroll_offset += 1

    def select_melody(self, index):
        if 0 <= index < len(self.all_melodies):
            self.current_melody_index = index
            self.current_melody_data = self.all_melodies[index]
            return True
        return False

    def select_melody_by_click(self, mouse_pos):
        list_rect = pygame.Rect(MELODY_LIST_X, MELODY_LIST_Y,
                                MELODY_LIST_WIDTH, MELODY_LIST_HEIGHT)

        if list_rect.collidepoint(mouse_pos):
            rel_y = mouse_pos[1] - MELODY_LIST_Y
            clicked_index = self.list_scroll_offset + (rel_y // MELODY_ITEM_HEIGHT)

            if 0 <= clicked_index < len(self.all_melodies):
                self.select_melody(clicked_index)
                return True

        return False

    def start_recording(self):
        self.recording = True
        self.record_start_time = pygame.time.get_ticks()
        self.recorded_notes = []
        self.last_note_time = 0
        self.record_control_button.text = "ОСТАНОВИТЬ"

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.record_control_button.text = "НАЧАТЬ ЗАПИСЬ"
            return True
        return False

    def toggle_recording(self):
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()

    def record_note(self, note_name):
        if not self.recording:
            return

        current_time = pygame.time.get_ticks()
        time_since_start = current_time - self.record_start_time

        note_data = {
            'note': note_name,
            'time': time_since_start,
            'delay': time_since_start - self.last_note_time if self.recorded_notes else 0
        }

        self.recorded_notes.append(note_data)
        self.last_note_time = time_since_start

    def save_melody(self):
        if not self.recorded_notes:
            return False

        notes_with_delay = []
        prev_time = 0
        for note in self.recorded_notes:
            delay = note['time'] - prev_time
            notes_with_delay.append({
                'note': note['note'],
                'delay': delay
            })
            prev_time = note['time']

        timestamp = datetime.now().strftime("%H%M%S")

        melody_data = {
            'name': f"{timestamp}",
            'flag': 0,
            'notes': notes_with_delay
        }
        add_mel_json('melodies/mel.json', melody_data)
        self.all_melodies = read_json('melodies/mel.json')
        if self.all_melodies:
            self.select_melody(len(self.all_melodies) - 1)

        return True

    def convert_current_to_wav(self):
        if self.all_melodies and self.current_melody_index < len(self.all_melodies):
            melody = self.all_melodies[self.current_melody_index]
            if melody.get('notes'):
                self.convert_json_to_wav(melody)
            else:
                print("У выбранной мелодии нет нот!")
        else:
            print("Нет выбранной мелодии!")

    def start_playback(self):
        if not self.all_melodies or self.current_melody_index >= len(self.all_melodies):
            return

        melody = self.all_melodies[self.current_melody_index]
        self.current_playback_notes = melody.get('notes', [])

        if not self.current_playback_notes:
            return

        self.playing = True
        self.playback_index = 0
        self.playback_start_time = pygame.time.get_ticks()
        self.playback_note_start_time = 0
        self.play_button.text = "ОСТАНОВИТЬ"

    def stop_playback(self):
        self.playing = False
        self.playback_index = 0
        self.current_playback_notes = []
        self.play_button.text = "ВОСПРОИЗВЕСТИ"

    def toggle_playback(self):
        if not self.playing:
            self.start_playback()
        else:
            self.stop_playback()

    def update_playback(self):
        if not self.playing or not self.current_playback_notes:
            return

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.playback_start_time

        if self.playback_index < len(self.current_playback_notes):
            note_data = self.current_playback_notes[self.playback_index]
            note_delay = note_data.get('delay', 0)

            if elapsed >= self.playback_note_start_time + note_delay:
                note_name = note_data.get('note', '')
                if note_name in self.current_sounds and self.current_sounds[note_name]:
                    self.current_sounds[note_name].play()

                    if note_name in KEY_LABELS:
                        index = KEY_LABELS.index(note_name)
                        self.key_glow_time[index] = current_time

                self.playback_index += 1
                self.playback_note_start_time = elapsed

                if self.playback_index >= len(self.current_playback_notes):
                    self.stop_playback()
        else:
            self.stop_playback()

    def delete_selected_melody(self):
        if not self.all_melodies or self.current_melody_index >= len(self.all_melodies):
            return False

        melody_name = self.all_melodies[self.current_melody_index].get('name', '')

        if delete_melody('melodies/mel.json', melody_name):
            self.all_melodies = read_json('melodies/mel.json')

            if self.all_melodies:
                self.current_melody_index = min(self.current_melody_index, len(self.all_melodies) - 1)
                self.current_melody_data = self.all_melodies[self.current_melody_index]
            else:
                self.current_melody_index = 0
                self.current_melody_data = {'name': 'Нет мелодий', 'flag': 0, 'notes': []}

            return True

        return False

    def handle_events(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                return False

            if self.record_button.handle_event(event):
                self.need_switch_to_normal = True
                continue

            if self.mode_button_game.handle_event(event):
                continue

            if self.up_button.handle_event(event):
                self.scroll_list("up")
                continue

            if self.down_button.handle_event(event):
                self.scroll_list("down")
                continue

            if self.record_control_button.handle_event(event):
                self.toggle_recording()
                continue

            if self.save_button.handle_event(event):
                self.save_melody()
                continue

            if self.convert_wav_button.handle_event(event):
                self.convert_current_to_wav()
                continue

            if self.play_button.handle_event(event):
                self.toggle_playback()
                continue

            if self.del_button.handle_event(event):
                self.delete_selected_melody()
                continue

            if self.mode_button.handle_event(event):
                self.switch_mode()
                continue

            if self.exit_button.handle_event(event):
                pygame.time.delay(130)
                return False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.select_melody_by_click(pygame.mouse.get_pos())

            elif event.type == pygame.KEYDOWN:
                note_name = self.get_note_from_key(event.key)
                if note_name:
                    self.play_note(note_name)

                    if self.recording:
                        self.record_note(note_name)

        return True

    def get_note_from_key(self, key):
        note_mapping = {
            pygame.K_s: 'S',
            pygame.K_d: 'D',
            pygame.K_f: 'F',
            pygame.K_g: 'G',
            pygame.K_h: 'H',
            pygame.K_j: 'J',
            pygame.K_k: 'K',
        }
        return note_mapping.get(key)

    def play_note(self, note_name):
        if note_name in self.current_sounds and self.current_sounds[note_name]:
            self.current_sounds[note_name].play()

        if note_name in KEY_LABELS:
            index = KEY_LABELS.index(note_name)
            self.key_glow_time[index] = pygame.time.get_ticks()

    def update(self):
        super().update()
        self.update_playback()

        mouse_pos = pygame.mouse.get_pos()
        self.up_button.check_hover(mouse_pos)
        self.down_button.check_hover(mouse_pos)

        for button in self.control_buttons:
            button.check_hover(mouse_pos)

    def draw_melody_list(self):
        pygame.draw.rect(self.screen, MELODY_LIST_BG_COLOR,
                         (MELODY_LIST_X, MELODY_LIST_Y,
                          MELODY_LIST_WIDTH, MELODY_LIST_HEIGHT))

        font = pygame.font.SysFont(FONT, SIZE_TEXT)
        title = font.render("СПИСОК МЕЛОДИЙ:", True, TEXT)
        self.screen.blit(title, (MELODY_LIST_X + 10, MELODY_LIST_Y - 30))

        start_idx = self.list_scroll_offset
        end_idx = min(start_idx + MAX_VISIBLE_MELODIES, len(self.all_melodies))

        for i in range(start_idx, end_idx):
            melody = self.all_melodies[i]
            y_pos = MELODY_LIST_Y + (i - start_idx) * MELODY_ITEM_HEIGHT

            if i == self.current_melody_index:
                pygame.draw.rect(self.screen, MELODY_SELECTED_COLOR,
                                 (MELODY_LIST_X, y_pos, MELODY_LIST_WIDTH - 40, MELODY_ITEM_HEIGHT))
                text_color = TEXT
            else:
                text_color = MELODY_NORMAL_COLOR

            name = melody.get('name')
            text = font.render(name, True, text_color)
            self.screen.blit(text, (MELODY_LIST_X + 20, y_pos + 5))

        self.up_button.draw(self.screen)
        self.down_button.draw(self.screen)

    def draw(self):
        super().draw()
        self.draw_melody_list()

        for button in self.control_buttons:
            button.draw(self.screen)

        font = pygame.font.SysFont(FONT, SIZE_TEXT)

        if self.recording:
            record_text = font.render("ЗАПИСЬ...", True, (255, 0, 0))
            self.screen.blit(record_text, (PIANO_START_X , PIANO_START_Y + KEY_HEIGHT + KEY_SPACING ))


        y_offset = MELODY_LIST_Y + MELODY_LIST_HEIGHT + 40

        if self.recorded_notes:
            notes_text = font.render(
                f"Записано нот: {len(self.recorded_notes)}",
                True, TEXT
            )
            self.screen.blit(notes_text, (MELODY_LIST_X, y_offset))
        else:
            no_notes_text = font.render("Нет записанных нот", True, (200, 200, 200))
            self.screen.blit(no_notes_text, (MELODY_LIST_X, y_offset))

        if self.all_melodies and self.current_melody_index < len(self.all_melodies):
            melody = self.all_melodies[self.current_melody_index]
            note_count = len(melody.get('notes', []))
            melody_type = "Встроенная" if melody.get('flag', 0) == 1 else "Пользовательская"

            selected_text = font.render(
                f"Выбрано: {melody.get('name', '')}",
                True, TEXT
            )

            info_text1 = font.render(
                f"Нот: {note_count} | Тип: {melody_type}",
                True, TEXT
            )

            self.screen.blit(selected_text, (RECORD_BUTTON_X -90 ,
                                             RECORD_BUTTON_Y + (BUTTON_HEIGHT + KEY_SPACING) * 2))
            self.screen.blit(info_text1, (RECORD_BUTTON_X-90,
                                          RECORD_BUTTON_Y + (BUTTON_HEIGHT + KEY_SPACING) * 3))

        self.draw_mode_game()

    def draw_mode_game(self):
        font = pygame.font.SysFont(FONT, SIZE_TEXT)
        mode_text = font.render(CURRENT_MODE_GAME[2], True, TEXT)
        self.screen.blit(mode_text, (MODE_TEXT_X, MODE_TEXT_Y + 35))

    def run(self):
        self.clock.tick(FPS)

        if not self.handle_events():
            return False

        self.update()
        self.draw()
        pygame.display.flip()

        return True
import pygame
from config import *
from scenes.piano import PianoScene
from scenes.falling_piano_scene import FallingPianoScene
from scenes.save_mode import MelodyRecorderScene


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(**SOUND_SETTINGS)
        pygame.mixer.set_num_channels(NUM_CHANNELS)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("MY PIANO")
        self.clock = pygame.time.Clock()
        self.running = True

        # Не храним сцены, создаем каждый раз
        self.current_scene = PianoScene(self.screen, self.clock)
        self.current_mode = "piano"

    def switch_scene(self, new_mode):
        """Переключает сцены (создает новые экземпляры)"""
        if new_mode == self.current_mode:
            return

        print(f"Переключаемся с {self.current_mode} на {new_mode}")

        if new_mode == "piano":
            # Всегда создаем новую сцену пианино
            self.current_scene = PianoScene(self.screen, self.clock)
        elif new_mode == "falling":
            self.current_scene = FallingPianoScene(self.screen, self.clock)
        elif new_mode == "recorder":
            self.current_scene = MelodyRecorderScene(self.screen, self.clock)

        self.current_mode = new_mode

    def run(self):
        while self.running:
            self.running = self.current_scene.run()

            # Проверяем флаги переключения
            if hasattr(self.current_scene, 'need_switch_to_game') and self.current_scene.need_switch_to_game:
                if self.current_mode == "piano":
                    self.switch_scene("falling")
                elif self.current_mode == "falling":
                    self.switch_scene("piano")
                # Флаг сбросится сам при создании новой сцены


            elif hasattr(self.current_scene, 'need_switch_to_record') and self.current_scene.need_switch_to_record:
                if self.current_mode == "piano":
                    self.switch_scene("recorder")


            elif hasattr(self.current_scene, 'need_switch_to_normal') and self.current_scene.need_switch_to_normal:
                if self.current_mode == "recorder":
                    self.switch_scene("piano")

        pygame.quit()

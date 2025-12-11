import pygame
from config import *
from scenes.piano import PianoScene
from scenes.falling_piano_scene import FallingPianoScene

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(**SOUND_SETTINGS)
        pygame.mixer.set_num_channels(NUM_CHANNELS)

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("MY PIANO")
        self.clock = pygame.time.Clock()
        self.running = True

        # Начинаем с обычного пианино
        self.current_scene = PianoScene(self.screen, self.clock)
        self.is_game_mode = False  # Флаг игрового режима

    def switch_to_game_mode(self):
        """Переключает на игровой режим"""
        if not self.is_game_mode:
            self.current_scene = FallingPianoScene(self.screen, self.clock)
            self.is_game_mode = True
        else:
            self.current_scene = PianoScene(self.screen, self.clock)
            self.is_game_mode = False

    def run(self):
        while self.running:
            self.running = self.current_scene.run()

            if hasattr(self.current_scene, 'need_switch_to_game') and self.current_scene.need_switch_to_game:
                self.switch_to_game_mode()
                self.current_scene.need_switch_to_game = False

        pygame.quit()

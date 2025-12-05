# core/game.py
import pygame
from config import *
from scenes.piano import PianoScene

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init(**SOUND_SETTINGS)
        pygame.mixer.set_num_channels(NUM_CHANNELS)

        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption("MY PIANO")
        self.clock = pygame.time.Clock()
        self.running = True

    def run(self):
        piano_scene = PianoScene(self.screen, self.clock)

        while self.running:
            self.running = piano_scene.run()

        pygame.quit()
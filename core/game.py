import pygame
import os
from datetime import datetime
from utils.config import *
from scenes.license_scene import LicenseScene
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

        self.license_file = "piano_subscription.txt"
        self.access_granted = self.check_subscription()
        self.is_premium = self.access_granted

        if self.access_granted:
            self.current_scene = PianoScene(self.screen, self.clock)
            self.current_mode = "piano"
        else:
            self.license_scene = LicenseScene(self.screen, self.clock)
            self.current_scene = self.license_scene
            self.current_mode = "license"

    def check_subscription(self):
        if not os.path.exists(self.license_file):
            return False

        try:
            with open(self.license_file, 'r') as f:
                start_date_str = f.read().strip()

            if not start_date_str:
                os.remove(self.license_file)
                return False

            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            current_date = datetime.now()
            days_passed = (current_date - start_date).days

            if days_passed >= 30:
                os.remove(self.license_file)
                return False
            else:
                return True

        except Exception as e:
            if os.path.exists(self.license_file):
                os.remove(self.license_file)
            return False

    def switch_scene(self, new_mode):
        if new_mode == self.current_mode:
            return

        if new_mode == "license":
            self.current_scene = LicenseScene(self.screen, self.clock)
        elif new_mode == "piano":
            self.current_scene = PianoScene(self.screen, self.clock)
        elif new_mode == "falling":
            self.current_scene = FallingPianoScene(self.screen, self.clock)
        elif new_mode == "recorder":
            self.current_scene = MelodyRecorderScene(self.screen, self.clock)

        self.current_mode = new_mode

    def apply_restrictions(self):
        if not self.is_premium:
            pass

    def check_premium_features(self, feature_name):
        if not self.is_premium:
            return False
        return True

    def run(self):
        while self.running:
            if not self.access_granted:
                self.running = self.license_scene.run()

                if hasattr(self.license_scene, 'verified') and self.license_scene.verified:
                    self.access_granted = True
                    self.is_premium = True

                    self.switch_scene("piano")
                    self.apply_restrictions()
                else:
                    continue

            self.running = self.current_scene.run()

            if hasattr(self.current_scene, 'need_switch_to_game') and self.current_scene.need_switch_to_game:
                if self.current_mode == "piano":
                    self.switch_scene("falling")
                elif self.current_mode == "falling":
                    self.switch_scene("piano")

            elif hasattr(self.current_scene, 'need_switch_to_record') and self.current_scene.need_switch_to_record:
                if self.current_mode == "piano" or self.current_mode == "falling":
                    self.switch_scene("recorder")

            elif hasattr(self.current_scene, 'need_switch_to_normal') and self.current_scene.need_switch_to_normal:
                if self.current_mode == "recorder":
                    self.switch_scene("piano")

            elif hasattr(self.current_scene, 'need_exit_to_license'):
                self.access_granted = False
                self.is_premium = False
                self.switch_scene("license")

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
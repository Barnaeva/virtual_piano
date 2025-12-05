import pygame
from core.game import Game

def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Ошибка запуска: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")

if __name__ == "__main__":
    main()
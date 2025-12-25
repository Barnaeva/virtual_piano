from core.game import Game
import sys
import traceback

def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Ошибка запуска: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
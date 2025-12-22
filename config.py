# =============== ОСНОВНЫЕ РАЗМЕРЫ ===============
WIDTH = 900
HEIGHT = 800
FPS = 30

# =============== ЦВЕТА ===============
BACKGROUND = (50, 50, 50)
BUTTON = (100, 100, 100)          # Светло-серый - кнопки
KEYS_PIANO = (200, 200, 200)      # Серый - подсветка клавиш
TEXT = (255, 255, 255)

# =============== ПИАНИНО ===============
KEY_COUNT = 7
KEY_LABELS = ['S', 'D', 'F', 'G', 'H', 'J', 'K']

# Размеры клавиш
KEY_WIDTH = 100
KEY_HEIGHT = 200
KEY_SPACING = 5

# Позиция пианино
PIANO_START_X = (WIDTH - (KEY_COUNT * KEY_WIDTH + (KEY_COUNT - 1) * KEY_SPACING)) // 2
PIANO_START_Y = HEIGHT * 0.65

# Текст на клавишах
KEY_TEXT_OFFSET_X = KEY_WIDTH // 2 - 5
KEY_TEXT_OFFSET_Y = KEY_HEIGHT // 2 - 10

# Подсветка клавиш
GLOW_DURATION = 300

# =============== КНОПКИ ОСНОВНОГО РЕЖИМА ===============
# Размеры кнопок
BUTTON_WIDTH = 230
BUTTON_HEIGHT = 35
EXIT_BUTTON_WIDTH = 150
EXIT_BUTTON_HEIGHT = 35

# Кнопка режима звука
MODE_BUTTON_X = PIANO_START_X
MODE_BUTTON_Y = HEIGHT * 0.05

# Кнопка режима игры
MODE_GAME_BUTTON_X = PIANO_START_X
MODE_GAME_BUTTON_Y = HEIGHT * 0.1

# Кнопка выхода
EXIT_BUTTON_X = WIDTH - EXIT_BUTTON_WIDTH - PIANO_START_X
EXIT_BUTTON_Y = HEIGHT * 0.05

# Кнопка записи/воспроизведения
RECORD_BUTTON_X = WIDTH - BUTTON_WIDTH - PIANO_START_X
RECORD_BUTTON_Y = HEIGHT * 0.1

# Текст режимов
MODE_TEXT_X = MODE_BUTTON_X + BUTTON_WIDTH + KEY_SPACING
MODE_TEXT_Y = HEIGHT * 0.06

# =============== КНОПКИ РЕЖИМА ПАДАЮЩИХ НОТ ===============
GAME_BUTTON_WIDTH = 120
GAME_BUTTON_HEIGHT = 37
GAME_BUTTON_SPACING = 5
START_BUTTON_WIDTH = 100

# Позиция кнопок падающих нот
GAME_BUTTON_X = MODE_BUTTON_X
GAME_BUTTON_Y = 210 - KEY_SPACING - GAME_BUTTON_HEIGHT

# =============== РЕЖИМ ПАДАЮЩИХ НОТ ===============
# Падающие ноты
FALLING_NOTES_START_Y = 200  # Начальная Y-координата падающих нот
FALLING_NOTE_HEIGHT = 50     # Высота падающей ноты
FALLING_SPEED = 5            # Скорость падения нот

# Область для падающих нот
NOTES_AREA_START_Y = 210            # Начало области
NOTES_AREA_HEIGHT = 310             # Высота области
NOTES_AREA_COLOR = (230, 230, 230)  # Цвет области падающих нот

# Зона попадания
HIT_ZONE_ALPHA = 100         # Прозрачность зоны попадания (0-255)
HIT_ZONE_COLOR = (170, 200, 170)  # Цвет зоны попадания (светло-зеленый)
HIT_ZONE_BORDER_COLOR = (170, 200, 170)  # Цвет границы зоны

# Внешний вид падающих нот
FALLING_NOTE_COLOR = BUTTON         # Цвет обычной ноты
FALLING_NOTE_HIT_COLOR = (0, 255, 0)  # Цвет при попадании (зеленый)
FALLING_NOTE_TEXT_COLOR = TEXT      # Цвет текста на ноте
FALLING_NOTE_FONT_SIZE = 24         # Размер шрифта на ноте

# Очки
SCORE_PER_HIT = 100                 # Очков за попадание

# Цвета статистики
SCORE_COLOR = (0, 255, 0)    # Цвет счета (зеленый)
MISSES_COLOR = (255, 0, 0)   # Цвет промахов (красный)

# Позиции текста статистики
TEXT_OFFSET_X = PIANO_START_X + KEY_SPACING
TEXT_OFFSET_Y = HEIGHT * 0.15
SCORE_POS_X_OFFSET = 250     # Смещение по X для счета
MISSES_POS_X_OFFSET = 400    # Смещение по X для промахов
PROGRESS_POS_Y = 100         # Y-позиция для прогресса

# Инструкция
INSTRUCTION_TEXT = "Нажимайте клавиши когда ноты в зеленой зоне!"
INSTRUCTION_POS_Y = HEIGHT - 70  # Y-позиция инструкции

# Текст режима игры
MODE_GAME_TEXT = " ПАДАЮЩИЕ НОТЫ"

# Кнопка мелодии (начальный текст)
MEL_BUTTON_TEXT = "Гуси"  # Начальный текст (будет меняться)

# =============== РЕЖИМ ЗАПИСИ МЕЛОДИЙ ===============
# Список мелодий
MELODY_LIST_X = PIANO_START_X
MELODY_LIST_Y = 150
MELODY_LIST_WIDTH = 400
MELODY_LIST_HEIGHT = 300
MELODY_ITEM_HEIGHT = 30
MAX_VISIBLE_MELODIES = 10  # Сколько мелодий показывать за раз

# Цвета списка мелодий
MELODY_LIST_BG_COLOR = (70, 70, 70)
MELODY_SELECTED_COLOR = (100, 150, 200)
MELODY_NORMAL_COLOR = TEXT

# =============== ЗВУК ===============
SOUND_SETTINGS = {
    'frequency': 22050,
    'size': -16,
    'channels': 2,
    'buffer': 512
}
NUM_CHANNELS = 16
BUTTON_SOUND_PATH = "sounds/click.wav"

# Звуковые режимы
SOUND_PATHS = {
    "1": {
        'S': "sounds/grandpiano/do.wav",
        'D': "sounds/grandpiano/re.wav",
        'F': "sounds/grandpiano/mi.wav",
        'G': "sounds/grandpiano/fa.wav",
        'H': "sounds/grandpiano/salt.wav",
        'J': "sounds/grandpiano/la.wav",
        'K': "sounds/grandpiano/si.wav"
    },
    "2": {
        'S': "sounds/piano/do.wav",
        'D': "sounds/piano/re.wav",
        'F': "sounds/piano/mi.wav",
        'G': "sounds/piano/fa.wav",
        'H': "sounds/piano/salt.wav",
        'J': "sounds/piano/la.wav",
        'K': "sounds/piano/si.wav"
    },
    "3": {
        'S': "sounds/bam/do.wav",
        'D': "sounds/bam/re.wav",
        'F': "sounds/bam/mi.wav",
        'G': "sounds/bam/fa.wav",
        'H': "sounds/bam/salt.wav",
        'J': "sounds/bam/la.wav",
        'K': "sounds/bam/si.wav"
    }
}

# Названия звуковых режимов
CURRENT_MODE = {"1": 'РОЯЛЬ', "2": 'ПИАНИНО', "3": 'УДАРНЫЕ'}

# =============== РЕЖИМЫ ИГРЫ ===============
CURRENT_MODE_GAME = ["СИНТЕЗАТОР", "ПАДАЮЩИЕ НОТЫ", "ЗАПИСЬ МЕЛОДИИ"]

# =============== ШРИФТЫ ===============
FONT = 'timesnewroman'
SIZE_TEXT = 23

# =============== ЗАПИСЬ WAV ===============
DEFAULT_WAV_FILENAME = "my_melody.wav"
WAV_EXPORT_PATH = "melodies/"
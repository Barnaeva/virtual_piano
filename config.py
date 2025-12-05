from tkinter.constants import CURRENT

WIDTH = 900
HEIGHT = 800
KEY_COUNT = 7

KEY_WIDTH = 100
KEY_HEIGHT = 200
KEY_SPACING = 5
PIANO_START_X = (WIDTH - (KEY_COUNT * KEY_WIDTH + (KEY_COUNT - 1) * KEY_SPACING)) // 2
PIANO_START_Y = HEIGHT*0.5


KEY_TEXT_OFFSET_X = KEY_WIDTH//2 - 5
KEY_TEXT_OFFSET_Y = KEY_HEIGHT//2 - 10

MODE_TEXT_X = (WIDTH - (KEY_COUNT * KEY_WIDTH + (KEY_COUNT - 1) * KEY_SPACING)) // 2
MODE_TEXT_Y = HEIGHT*0.05

MODE_BUTTON_WIDTH = 250
MODE_BUTTON_HEIGHT = 50
MODE_BUTTON_X = WIDTH - MODE_BUTTON_WIDTH - PIANO_START_X
MODE_BUTTON_Y = HEIGHT*0.05

MODE_GAME_BUTTON_X=WIDTH - MODE_BUTTON_WIDTH - PIANO_START_X
MODE_GAME_BUTTON_Y=HEIGHT*0.12
MODE_GAME_BUTTON_WIDTH=250
MODE_GAME_BUTTON_HEIGHT=50

EXIT_BUTTON_WIDTH = 250
EXIT_BUTTON_HEIGHT = 50
EXIT_BUTTON_X =  WIDTH - EXIT_BUTTON_WIDTH - PIANO_START_X
EXIT_BUTTON_Y = HEIGHT*0.19

SIZE_TEXT=30
FONT='timesnewroman'

FPS = 30

BACKGROUND = (50, 50, 50)
BUTTON = (100, 100, 100)          # Светло-серый - кнопки
KEYS_PIANO = (200, 200, 200)      # Серый - подсветка клавиш
TEXT = (255, 255, 255)

SOUND_SETTINGS = {
    'frequency': 22050,
    'size': -16,
    'channels': 2,
    'buffer': 512
}
NUM_CHANNELS = 16
GLOW_DURATION = 300

BUTTON_SOUND_PATH="sounds/click.wav"
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
CURRENT_MODE={"1":'РОЯЛЬ',"2":'ПИАНИНО',"3":'УДАРНЫЕ'}

KEY_LABELS = ['S', 'D', 'F', 'G', 'H', 'J', 'K']

MELODY_GUSI=['G', 'F', 'D', 'S', 'H', 'H',
             'G', 'F', 'D', 'S', 'H', 'H',
             'G', 'J', 'J', 'G', 'F', 'H', 'H', 'F',
             'D','F','G','D','S','S',
             'G', 'J', 'J', 'G', 'F', 'H', 'H', 'F',
             'D','F','G','D','S','S']
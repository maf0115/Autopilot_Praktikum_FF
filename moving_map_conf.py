from pygame.image import load 
from pygame.display import set_mode
from pygame import RESIZABLE
from os import path
from random import uniform

# Images
MANCHING_MAP = load(path.join(".\Images", "Manching.png"))
WINDOW_LOGO = load(path.join(".\Images", "WindowLogo.png"))

# Screen Measurements
CANVAS_X = MANCHING_MAP.get_width()
CANVAS_Y = MANCHING_MAP.get_height()

# Colors 
TRACE_COLOR = (221, 25, 224)
BLACK = (0, 0, 0)
FIGTHER_JET_COLOR = (150, 255, 100)
WYP_COLOR = (8, 252, 252)
CONNECTION_COLOR = (255, 0, 0)
WHITE = (255, 255, 255)

# Map some coordinates to pixel values to get some reference points
# These coordinates were obtained by clicking on some specific coordinates on the image and getting the pixel values of the mouse cursor
MIN_X = (29/60, 250)
MAX_X = (35/60, 405)
MIN_Y = (50/60, 90) 
MAX_Y = (40/60, 480)

# Main window and game loop
SCREEN = set_mode((CANVAS_X * 2, CANVAS_Y), RESIZABLE)
RUNNING = True

# List to keep track of the jet's trail and all of the stuff it needs as well 
TRAIL_LIST = list()
TRAIL_MAX_LEN = 5
TRAIL_POINT_DISTANCE = 300
TRAIL_POINT_CNT = 0

# Waypoint list
WYP_LIST = list()
WYP_LIST_MAX_LEN = 12
WYP_CNT = 0

# Waypoint connection list
WYP_CONNECTION_LIST = list()
WYP_CONNECTION_LIST_MAX_LEN = WYP_LIST_MAX_LEN - 1
WYP_CONNECTION_CNT = 0

# Variables to keep track of the text lines
WYP_INFO_LINE_SIZE_Y = 25
TXT_CNT = 0
TXT_TAB = '   '

# Variables to draw the fighter jet
Y_DIST_COW = 13
BASE = 6.5

# Variables regarding wind 
WIND_SPEED = 10.0 * 1852.0 / 3600.0 
WD = 180.0
WIND_DIRECTION = (WD+ 180) % 360

# Variables to keep track of bogus data
BOG_LAT = uniform(11.0 + 29/60, 11.0 + 35/60)
BOG_LON = uniform(48.0 + 40/60, 48.0 + 50/60)
BOG_ALT = uniform(300 / 0.3841, 600 / 0.3841)
BOG_PITCH = 0
BOG_ROLL = 0
BOG_YAW = uniform(0, 359)
TICK_CNT = 0

# Autopilot
CURRENT_CONNECTION_INDEX = 0


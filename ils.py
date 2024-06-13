# Pygame imports
from pygame import init, QUIT, KEYDOWN, K_ESCAPE, quit
from pygame import event
from pygame.draw import circle, rect, line
from pygame import font, Rect
from pygame import display, RESIZABLE 
from pygame.image import load
from pygame.math import Vector2

# Native pyhon imports
from os import path
from math import degrees, cos, atan2

# Images
WINDOW_LOGO = load(path.join(".\Images", "ILS_Icon.png"))

# Screen Measurements
CANVAS_SIZE = 800
CIRCLE_RADIUS = CANVAS_SIZE/2 - 50
CENTER = (CANVAS_SIZE/2, CANVAS_SIZE/2)

# Reference points macros
REF_POINT_AMT = 6
REF_POINT_DIST = CIRCLE_RADIUS/REF_POINT_AMT
REF_POINT_RADIUS = 10

# INOP flag measurements
INOP_SIDE_X = 150
INOP_SIDE_Y = 100
INOP_COORD_X = CANVAS_SIZE/2 + 2*REF_POINT_DIST
INOP_COORD_Y = CANVAS_SIZE/2 - 3*REF_POINT_DIST
INOP_DIST = 20

# Horizontal reference line coordinates (HOR. FLUGWEG)
HOR_REF_X_START = 125
HOR_REF_X_END = 675

# Vertical reference line coordinates (GLEITWINKEL)
VER_REF_Y_START = 125
VER_REF_Y_END =  675
MAX_DRIFT = 2.5

# FAF VADAN reference coordinates (lat, lon)
VADAN = (11.67508056, 48.74578056)

# Runway threshold coordinates (lat, lon, heigth)
RWY_THRESHOLD = (11.55578889, 48.71437778, 1253 * 0.3048)

# Colors
BLACK = (0, 0, 0)
SLOPE_INDICATOR_COLOR = (150, 255, 100)
ILS_BORDER_COLOR = (227, 225, 218)
INOP_FLAG_COLOR = (255, 0, 0)

# Main window and game loop
SCREEN = display.set_mode((CANVAS_SIZE, CANVAS_SIZE), RESIZABLE)
RUNNING = True

def setup_window_info()->None: 
    init()
    display.set_icon(WINDOW_LOGO)
    display.set_caption("Instrument Landing System (maf0115)")

def draw_ils()->None:
    SCREEN.fill(BLACK)
    circle(SCREEN, 
           ILS_BORDER_COLOR, 
           CENTER, 
           CIRCLE_RADIUS, 
           5)
    
    def draw_ref_points(start : tuple, vert_dir : int, hor_dir : int )->None:
        x_start = start[0]
        y_start = start[1]

        cnt = 0

        while cnt < REF_POINT_AMT:
            circle(SCREEN,
                    ILS_BORDER_COLOR, 
                    (x_start, y_start), 
                    REF_POINT_RADIUS)

            # Update coordinates
            cnt += 1
            x_start = CANVAS_SIZE/2 + abs(cnt * REF_POINT_DIST) * hor_dir
            y_start = CANVAS_SIZE/2 + abs(cnt * REF_POINT_DIST) * vert_dir
                 
    draw_ref_points(CENTER, 1, 0)
    draw_ref_points(CENTER, -1, 0)
    draw_ref_points(CENTER, 0, 1)
    draw_ref_points(CENTER, 0, -1)

def draw_inop_flag()->None: 
    inop_rect = Rect((INOP_COORD_X + INOP_DIST, 
                      INOP_COORD_Y + INOP_DIST, 
                      INOP_SIDE_X, 
                      INOP_SIDE_Y))
    
    text_surface_object = font.SysFont('Arial', 50).render('INOP', True, BLACK)

    text_rect = text_surface_object.get_rect(center = inop_rect.center)
    rect(SCREEN, INOP_FLAG_COLOR, inop_rect)
    SCREEN.blit(text_surface_object, text_rect)

def draw_horizontal_reference(sim_data : list = None)->None:
    line(SCREEN, 
         SLOPE_INDICATOR_COLOR, 
         (HOR_REF_X_START, CANVAS_SIZE/2), 
         (HOR_REF_X_END, CANVAS_SIZE/2), 
         7)

def draw_vertical_reference(sim_data : list = None)->None:
    def sign(num : float):
        if num > 0: return 1
        elif num < 0: return -1
        else: return 0

    # BAse the angle on real life calculations: trigonometry is your friend rn
    angle = 2.7
    print(f'angle: {angle}°')

    if abs(angle) < MAX_DRIFT: 
        x = CANVAS_SIZE/2 + (angle % MAX_DRIFT) * -REF_POINT_DIST
        # Based on the degrees, draw the line
        line(SCREEN, 
            SLOPE_INDICATOR_COLOR, 
            (x, VER_REF_Y_START), 
            (x, VER_REF_Y_END), 
            7)
    else:
        line(SCREEN, 
            SLOPE_INDICATOR_COLOR, 
            (CANVAS_SIZE/2 + REF_POINT_DIST * REF_POINT_AMT * -sign(angle), VER_REF_Y_START), 
            (CANVAS_SIZE/2 + REF_POINT_DIST * REF_POINT_AMT * -sign(angle), VER_REF_Y_END), 
            7)
        draw_inop_flag()
        

def test_main():
    setup_window_info()
    global RUNNING
    while RUNNING:
        for event_tmp in event.get(): 
            if event_tmp.type == QUIT: 
                RUNNING = False 

            # Events with keys
            elif event_tmp.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    RUNNING = False

        draw_ils()
        draw_horizontal_reference()
        draw_vertical_reference() 
        display.update()    
    quit()

if __name__ == '__main__': 
    test_main()
  
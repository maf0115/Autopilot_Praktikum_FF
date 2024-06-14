# Pygame imports
from pygame import init, QUIT, KEYDOWN, K_ESCAPE, quit
from pygame import event
from pygame.draw import circle, rect, line
from pygame import font, Rect
from pygame import display, RESIZABLE 
from pygame.image import load


# Native pyhon imports
from os import path
from math import acos, sin, cos, degrees, tan, pi

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
MAX_GLIDE = 0.72

# Vertical reference line coordinates (GLEITWINKEL)
VER_REF_Y_START = 125
VER_REF_Y_END =  675
MAX_DRIFT = 2.5

# FAF VADAN reference coordinates (lon, lat, heigth[m])
VADAN = (48.74578056, 11.67508056, 2900 * 0.3048)

# Runway threshold coordinates (lon, lat, heigth[m])
RWY_THRESHOLD = (48.71437778, 11.55578889, 1253 * 0.3048)

# Colors
BLACK = (0, 0, 0)
SLOPE_INDICATOR_COLOR = (150, 255, 100)
ILS_BORDER_COLOR = (227, 225, 218)
INOP_FLAG_COLOR = (255, 0, 0)

# Main window and game loop
SCREEN = display.set_mode((CANVAS_SIZE, CANVAS_SIZE), RESIZABLE)
RUNNING = True


# Helper functions to calculate distances
def get_dist_in_nm(point_1, point_2):
    dist_in_km = degrees(acos(sin(point_1[0])*sin(point_2[0]) + cos(point_1[0])*cos(point_2[0])*cos(point_2[1] - point_1[1])))

    return ((dist_in_km * pi/180) * 6378.157) / 1,852

def get_height_diff_in_nm(heigth_1, height_2): 
    return 1000 * (heigth_1 - height_2) / 1852


# Setup
def setup_window_info()->None: 
    init()
    display.set_icon(WINDOW_LOGO)
    display.set_caption("Instrument Landing System (maf0115)")
    
    global ANGLE_VADAN_RWY
    heigth_diff = get_height_diff_in_nm(VADAN[2], RWY_THRESHOLD[2])
    cathet = get_dist_in_nm(VADAN, RWY_THRESHOLD)

    ANGLE_VADAN_RWY = tan(heigth_diff/cathet)
    print(f'ANGLE_VADAN_RWY = {ANGLE_VADAN_RWY}')


# Drawing stuff
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
    height_diff = get_height_diff_in_nm(sim_data, RWY_THRESHOLD)
    cathet = get_dist_in_nm(sim_data, RWY_THRESHOLD)

    aircraft_angle = tan(height_diff/cathet) 
    
    angle_diff = ANGLE_VADAN_RWY - aircraft_angle
    if abs(angle_diff) < MAX_GLIDE:
        line(SCREEN, 
            SLOPE_INDICATOR_COLOR, 
            (HOR_REF_X_START, CANVAS_SIZE/2), 
            (HOR_REF_X_END, CANVAS_SIZE/2), 
            6)
    
    else: 
        line(SCREEN, 
            SLOPE_INDICATOR_COLOR, 
            (HOR_REF_X_START, 
             -angle_diff * REF_POINT_DIST * REF_POINT_AMT * CANVAS_SIZE/2), 
            (HOR_REF_X_END, 
             -angle_diff * REF_POINT_DIST * REF_POINT_AMT * CANVAS_SIZE/2), 
            6)
        draw_inop_flag()


def draw_vertical_reference(sim_data : list = None)->None:
    # Base the angle on real life calculations: trigonometry is your friend rn
    # How to do these calcs?
    if sim_data[0] > RWY_THRESHOLD[0]: 
        sign = 1
    else: 
        sign = -1

    hypothenuse = get_dist_in_nm(sim_data, RWY_THRESHOLD) 

    cathet = degrees(acos(sin(sim_data[0])*sin(sim_data[0]) + cos(sim_data[0])*cos(sim_data[0])*cos(RWY_THRESHOLD[1] - sim_data[1]))) 

    cathet = ((cathet *pi/180) * 6378.157) / 1,852

    angle = sign * cos(cathet/hypothenuse)
    print(f'angle: {angle}°')

    if abs(angle) < MAX_DRIFT: 
        x = CANVAS_SIZE/2 + (angle % MAX_DRIFT) * -REF_POINT_DIST
        # Based on the degrees, draw the line
        line(SCREEN, 
            SLOPE_INDICATOR_COLOR, 
            (x, VER_REF_Y_START), 
            (x, VER_REF_Y_END), 
            6)
    else:
        line(SCREEN, 
            SLOPE_INDICATOR_COLOR, 
            (CANVAS_SIZE/2 + REF_POINT_DIST * REF_POINT_AMT * -sign(angle), VER_REF_Y_START), 
            (CANVAS_SIZE/2 + REF_POINT_DIST * REF_POINT_AMT * -sign(angle), VER_REF_Y_END), 
            6)
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
  
import pygame
from pygame.draw import circle, rect
from pygame import font, Rect
from pygame import display, RESIZABLE 
from pygame.image import load
from os import path

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

# Colors
BLACK = (0, 0, 0)
SLOPE_INDICATOR_COLOR = (150, 255, 100)
ILS_BORDER_COLOR = (227, 225, 218)
INOP_FLAG_COLOR = (255, 0, 0)

# Map some coordinates to pixel values to get some reference points
# These coordinates were obtained by clicking on some specific coordinates on the image and getting the pixel values of the mouse cursor
MIN_X = (29/60, 250)
MAX_X = (35/60, 405)
MIN_Y = (50/60, 90) 
MAX_Y = (40/60, 480)

# Main window and game loop
SCREEN = display.set_mode((CANVAS_SIZE, CANVAS_SIZE), RESIZABLE)
RUNNING = True

def setup_window_info()->None: 
    pygame.init()
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

def test_main():
    setup_window_info()
    global RUNNING
    while RUNNING:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                RUNNING = False 

            # Events with keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False

        draw_ils()
        draw_inop_flag()
        display.update()

if __name__ == '__main__': 
    test_main()
  
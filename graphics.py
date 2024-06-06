import pygame
from pygame import display, RESIZABLE 
from pygame.image import load
from pygame.transform import scale
from os import path
import random

# Images
MANCHING_MAP = load(path.join(".\Images", "Manching.png"))
WINDOW_LOGO = load(path.join(".\Images", "WindowLogo.png"))

# Screen Measurements
CANVAS_X = MANCHING_MAP.get_width()
CANVAS_Y = MANCHING_MAP.get_height()


# Color for the trace to keep track of what pattern the aricraft flew
TRACE_COLOR = (221, 25, 224)
BLACK = (0, 0, 0)
FIGTHER_JET_COLOR = (150, 255, 100)

# Map some coordinates to pixel values to get some reference points
# These coordinates were obtained by clicking on some specific coordinates on the image and getting the pixel values of the mouse cursor
MIN_X = (29/60, 250)
MAX_X = (35/60, 405)
MIN_Y = (50/60, 90) 
MAX_Y = (40/60,  480)

# Main window and game loop
SCREEN = display.set_mode((CANVAS_X, CANVAS_Y), RESIZABLE)
RUNNING = True

# List to keep track of the jet's trail and all of the stuff it needs as well 
TRAIL_LIST = list()
TRAIL_MAX_LEN = 5
TRAIL_POINT_DISTANCE = 100

def setup_window_info()->None:   
    display.set_icon(WINDOW_LOGO)
    display.set_caption("Navigation System GUI (maf0115)") 

def generate_dummy_coordinates(): 
    return [random.uniform(11 + 20/60, 11 + 45/60), 
            random.uniform(48 + 36/60, 48 + 52/50),
            random.randint(0, 360)]

def get_coordinates(lat : float, lon : float)->tuple: 
    
    # 0 is for coordinates
    # 1 is for pixels 
    x = (((lat % 1) - MAX_X[0]) * (MAX_X[1] - MIN_X[1])) / (MAX_X[0] - MIN_X[0]) + MAX_X[1]

    # The problem with this coordinate is that the y-axis is not divided up uniformingly -> Get another inerval, both in coordinates and in pixel values
    y = (((lon % 1) - MAX_Y[0]) * (MAX_Y[1] - MIN_Y[1])) / (MAX_Y[0] - MIN_Y[0]) + MAX_Y[1] 

    print(f'x: {x}\ty: {y}')
    return (x, y)



def draw_fighter_jet(lat : float, lon : float, true_heading : float)->None: 
    """
    This function draws the fighter jet icon at a determined angle and coordinates 

    Args: 
        lat: the latitude (x-coordinate over Manching image)
        lon: the longitude (y-coordinate over Manching image)
        true_heading: the angle at which the image is to be drawn

    Returns: 
        None
    """
    coords = get_coordinates(lat, lon)
    fighter_jet = pygame.draw.polygon(SCREEN, [])


def dummy_main_loop()->None:
    """
    This function provides a dummy main loop to temporarely test the program functionality

    Args: 
        None
    Returns: 
        None
    """
    pygame.init()
    setup_window_info()
    RUNNING = True

    while RUNNING: 
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                RUNNING = False 

            # Events with keys
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    RUNNING = False
        
        # Get the coordinates for the current point
        # coords = generate_dummy_coordinates()
        converted_coords = get_coordinates(11.58333333, 48.66666667)


        # Display the reference image
        SCREEN.blit(scale(MANCHING_MAP, (CANVAS_X, CANVAS_Y)), (0, 0))

        # Display some reference lines to get good points for the x coordinate
        pygame.draw.line(SCREEN, 
                         TRACE_COLOR, 
                         (0, CANVAS_Y/2 - CANVAS_Y/24.5), 
                         (CANVAS_X, CANVAS_Y/2 - CANVAS_Y/24.5), 
                         2)

        # Draw point for reference
        pygame.draw.circle(SCREEN, BLACK, converted_coords, 5.0)

        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            mouse_pos = pygame.mouse.get_pos()
            print(f'mouse_x : {mouse_pos[0]}\tmouse_y: {mouse_pos[1]}')
        display.update()


if __name__ == '__main__': 
    dummy_main_loop()
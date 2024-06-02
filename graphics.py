import pygame
from pygame import display, RESIZABLE 
from pygame.image import load
from pygame.transform import scale
from os import path
import time

# Images
FIGHTER_JET = load(path.join(".\Images", "FighterJetIcon.png"))
MANCHING_MAP = load(path.join(".\Images", "Manching.png"))
WINDOW_LOGO = load(path.join(".\Images", "WindowLogo.png"))

# Screen Measurements
CANVAS_X = MANCHING_MAP.get_width()
CANVAS_Y = MANCHING_MAP.get_height()

# Color for the trace to keep track of what pattern the aricraft flew
TRACE_COLOR = (221, 25, 224)
BLACK = (0, 0, 0)

# Main window and game loop
SCREEN = display.set_mode((CANVAS_X, CANVAS_Y), RESIZABLE)

# Reference points for coordinate calculations
MINS_X = 25.0
MINS_Y = 12.0

def setup_window_info()->None:
    global RUNNING   
    display.set_icon(WINDOW_LOGO)
    display.set_caption("Navigation System GUI (maf0115)") 


def get_coordinates(lat : float, lon : float)->tuple: 
    """
    This function converts the given coordinates into pixels that will be displayed on the image. 

    Args: 
        lat: the given latitude
        lion: the given longitude
    Returns: 
        Tuple (x, y)
    """
    # lat starts from 11° 20' to 11° 45' 
    x = ((lat - 11) * 60 * CANVAS_X) / MINS_X
    y = ((lon - 48) * 60 * CANVAS_Y) / MINS_Y

    print(f'CANVAS_X : {CANVAS_X}\tCANVAS_Y: {CANVAS_Y}')
    print(f'x : {x}\ty:{y}')

    return (x, y)

    # lon starts from 48° 52' to 48° 36'


def draw_fighter_jet(lat : float, lon : float, true_heading : float)->None: 
    """
    This function draws the fighter jet icon at a determined angle and coordinates 

    Args: 
        lat: the latitude (x-coordinate over Manching image)
        lon: the longitude (y-coordinate over Manching image)
        true_heading: the angle at which the image is to be drawn

    Returns: 
        tuple containing x for lat and y for lon
    """



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
        
        # Get the coordinates for the current point
        coords = get_coordinates(11.5, 48.71666)

        # Display the reference image
        SCREEN.blit(scale(MANCHING_MAP, (CANVAS_X, CANVAS_Y)), (0, 0))
        pygame.draw.line(SCREEN, 
                         TRACE_COLOR, 
                         (CANVAS_X/2, 0),
                         (CANVAS_X/2,CANVAS_Y), 5)
        
        pygame.draw.line(SCREEN, 
                         TRACE_COLOR, 
                         (0, CANVAS_Y/2),
                         (CANVAS_X,CANVAS_Y/2), 5)
        
        pygame.draw.circle(SCREEN, BLACK, coords, 5.0)
        
        display.update()
        time.sleep(10)

if __name__ == '__main__': 
    dummy_main_loop()
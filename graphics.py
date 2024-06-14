import pygame
from pygame import display, RESIZABLE 
from pygame.image import load
from pygame.transform import scale
from pygame.math import Vector2
from pygame import Rect, font

from os import path
 

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
WYP_COLOR = (235, 55, 52)
WHITE = (255, 255, 255)

# Map some coordinates to pixel values to get some reference points
# These coordinates were obtained by clicking on some specific coordinates on the image and getting the pixel values of the mouse cursor
MIN_X = (29/60, 250)
MAX_X = (35/60, 405)
MIN_Y = (50/60, 90) 
MAX_Y = (40/60, 480)

# Main window and game loop
SCREEN = display.set_mode((CANVAS_X * 2, CANVAS_Y), RESIZABLE)
RUNNING = True

# List to keep track of the jet's trail and all of the stuff it needs as well 
TRAIL_LIST = list()
TRAIL_MAX_LEN = 5
TRAIL_POINT_DISTANCE = 100
TRAIL_POINT_CNT = 0

# Waypoint list
WYP_LIST = list()
WYP_LIST_MAX_LEN = 12
WYP_CNT = 0
LINE_SIZE_Y = 50

# Variables to draw the fighter jet
Y_DIST_COW = 13
BASE = 6.5

# Variables regarding wind 
GROUND_SPEED = 100.0 * 1852.0 / 3600.0 

# Put the waypoints in a class
class Waypoint: 
    def __init__(self, lon, lat): 
        self.lon = lon
        self.lat = lat

        self.x , self.y = get_coordinates((self.lon, self.lat))

        self.ui_wyp = Rect(lon - 3, lat - 3, 7, 7)


def setup_window_info()->None:   
    display.set_icon(WINDOW_LOGO)
    display.set_caption("Navigation System GUI (maf0115)") 

def get_coordinates(sim_data)->tuple:    
    # 0 is for coordinates
    # 1 is for pixels 
    lat = sim_data[1]
    lon = sim_data[0]
    return(
        (((lat % 1) - MAX_X[0]) * (MAX_X[1] - MIN_X[1])) / (MAX_X[0] - MIN_X[0]) + MAX_X[1],
        (((lon % 1) - MAX_Y[0]) * (MAX_Y[1] - MIN_Y[1])) / (MAX_Y[0] - MIN_Y[0]) + MAX_Y[1]
        )

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

    triangle_filling = [(lat, lon - Y_DIST_COW), 
                        (lat - BASE , lon +  Y_DIST_COW), 
                        (lat + BASE , lon +  Y_DIST_COW)]
    
    pp = Vector2((lat, lon))
    rotated_triangle = [
        (pygame.math.Vector2(x, y) - pp).rotate(true_heading) + pp for x, y in triangle_filling]
                          
    pygame.draw.polygon(SCREEN, 
                        TRACE_COLOR,
                        rotated_triangle, 
                        0) 

def draw_trail(lat : float, lon : float)->None:
    """
    This function ups a counter to keep track of how many points are rendered. for every TAIL_POINT_DISTANCE points, it saves the coodinates of said point in the list and displays it. The point gets then eliminated once the list adds another point and it reached TRAIL_MAX_LEN 

    Args: 

    Returns: 
        None
    """ 
    global TRAIL_POINT_CNT
    global TRAIL_POINT_DISTANCE
    global TRAIL_LIST
    global TRAIL_MAX_LEN

    if TRAIL_POINT_CNT >= TRAIL_POINT_DISTANCE: 
        if len(TRAIL_LIST) == TRAIL_MAX_LEN: 
            TRAIL_LIST.pop(0)
        TRAIL_LIST.append((lat, lon))
        TRAIL_POINT_CNT = 0
    else: 
        TRAIL_POINT_CNT += 1

    # Render the points
    for point in TRAIL_LIST: 
        pygame.draw.circle(SCREEN,
                           TRACE_COLOR, 
                           point, 
                           5)

def update_wyp_list(coords : tuple):
    if len(WYP_LIST) < WYP_LIST_MAX_LEN:
        WYP_LIST.append(Waypoint(coords[0], coords[1]))
    else: 
        print('List full!')

def draw_wyp_list_and_info(): 
    cnt = 0
    for wyp in WYP_LIST: 
        pygame.draw.rect(SCREEN, 
                         WYP_COLOR, 
                         wyp.ui_wyp)
        display_single_wyp_data(wyp, cnt)
        cnt += 1

def display_single_wyp_data(wyp_obj, cnt): 
    """
    This function displays the waypoint information on the right side of the screen 

    Args: 
        None
    Returns: 
        None
    """
    y = (cnt + 1) * LINE_SIZE_Y
    text = f'WP{WYP_CNT} -> lat: {wyp_obj.lat}     lon: {wyp_obj.lon}'
    text_surface_object = font.SysFont('Arial', 15).render(text, True, WHITE)
    text_rect = text_surface_object.get_rect(center = (4/3 * CANVAS_X, y))
    SCREEN.blit(text_surface_object, text_rect)


def draw_scene(sim_data : list)->None: 
    """
    This function draws the scene, including the main map, the fighter jet and the list of points

    Args: 
        sim_data: the simulation data 
    """

    # Display the reference image
    SCREEN.blit(scale(MANCHING_MAP, (CANVAS_X, CANVAS_Y)), (0, 0))

    # Convert the coordinates of the jet for every function that needs them
    lat, lon = get_coordinates(sim_data)

    # Draw fighter jet icon
    draw_fighter_jet(lat, lon, sim_data[5])

    # Render the trail
    draw_trail(lat, lon)

    draw_wyp_list_and_info()

    # Update the screen info
    display.update()
  
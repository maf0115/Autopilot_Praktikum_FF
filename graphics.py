from pygame import init, quit
from pygame import display
from pygame.transform import scale
from pygame.math import Vector2
from pygame import font
from pygame.draw import polygon, rect, circle, line

from wyp import Waypoint, Connection
import moving_map_conf as mmc

# Test modules
from pygame import event as ev
from pygame.mouse import get_pos
from pygame import KEYDOWN, K_ESCAPE, MOUSEBUTTONUP, QUIT, quit


def bogus_data()->list: 
    """
    Function to generate bogus data in the absence of the simulator

    Args: 
        None
    Returns: 
        list containing six information slots to simulate the data
    """
    incr_x = 1 if mmc.BOG_LAT <= 11.0 + 34/60 else -1
    incr_y = 1 if mmc.BOG_LON <= 48.0 + 44/60 else -1
    mmc.TICK_CNT += 1
    return [
        mmc.BOG_LON + incr_y * mmc.TICK_CNT, 
        mmc.BOG_LAT + incr_x * mmc.TICK_CNT, 
        mmc.BOG_ALT,
        mmc.BOG_PITCH, 
        mmc.BOG_ROLL, 
        mmc.BOG_YAW
    ]

def setup_window_info()->None:   
    display.set_icon(mmc.WINDOW_LOGO)
    display.set_caption("Navigation System GUI (maf0115)") 


def get_coordinates(sim_data)->tuple:
    """
    This function returns coordinates converted from GPS coordinates into a pixel value

    Args: 
        sim_data: an array containing the values sent by the simulator 

    Returns: 
        a tuple containing the converted coordinates (x, y) in pixel values
    """    
    lat = sim_data[1]
    lon = sim_data[0]
    return(
        (((lat % 1) - mmc.MAX_X[0]) * (mmc.MAX_X[1] - mmc.MIN_X[1])) / (mmc.MAX_X[0] - mmc.MIN_X[0]) + mmc.MAX_X[1],
        (((lon % 1) - mmc.MAX_Y[0]) * (mmc.MAX_Y[1] - mmc.MIN_Y[1])) / (mmc.MAX_Y[0] - mmc.MIN_Y[0]) + mmc.MAX_Y[1]
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

    triangle_filling = [(lat, lon - mmc.Y_DIST_COW), 
                        (lat - mmc.BASE , lon +  mmc.Y_DIST_COW), 
                        (lat + mmc.BASE , lon +  mmc.Y_DIST_COW)]
    
    pp = Vector2((lat, lon))
    rotated_triangle = [(Vector2(x, y) - pp).rotate(true_heading) + pp for x, y in triangle_filling]
                          
    polygon(mmc.SCREEN, 
            mmc.TRACE_COLOR,
            rotated_triangle, 
            0) 


def draw_trail(lat : float, lon : float)->None:
    """
    This function ups a counter to keep track of how many points are rendered. for every TAIL_POINT_DISTANCE points, it saves the coodinates of said point in the list and displays it. The point gets then eliminated once the list adds another point and it reached TRAIL_MAX_LEN 

    Args: 

    Returns: 
        None
    """ 
    # global TRAIL_POINT_CNT
    # global TRAIL_POINT_DISTANCE
    # global TRAIL_LIST
    # global TRAIL_MAX_LEN

    if mmc.TRAIL_POINT_CNT >= mmc.TRAIL_POINT_DISTANCE: 
        if len(mmc.TRAIL_LIST) == mmc.TRAIL_MAX_LEN: 
            mmc.TRAIL_LIST.pop(0)
        mmc.TRAIL_LIST.append((lat, lon))
        mmc.TRAIL_POINT_CNT = 0
    else: 
        mmc.TRAIL_POINT_CNT += 1

    # Render the points
    for point in mmc.TRAIL_LIST: 
        circle(mmc.SCREEN,
                           mmc.TRACE_COLOR, 
                           point, 
                           5)


def display_data():
    """
    This function displays information about the passed object on the right side of the screen

    Args: 
        wyp_obj: the waypoint object of which data needs to be displayed
        txt_color: the color that the text should be displayed in. Varies between waypoint and connection text
    Returns: 
        None
    """ 
    if len(mmc.TXT_LIST) > 0:
        mmc.TXT_CNT = 0
        for text in mmc.TXT_LIST:
            y = (mmc.TXT_CNT + 0.5) * mmc.WYP_INFO_LINE_SIZE_Y
            text_surface_object = font.SysFont('Arial', 15).render(text, False, mmc.WHITE)
            text_rect = text_surface_object.get_rect(center = (4/3 * mmc.CANVAS_X + 50, y))
            mmc.TXT_CNT += 1
        mmc.SCREEN.blit(text_surface_object, text_rect)


# WAYPOINTS

def update_wyp_list(coords : tuple)->None:
    if len(mmc.WYP_LIST) < mmc.WYP_LIST_MAX_LEN:
        tmp = Waypoint(coords[0], coords[1])
        tmp.set_wyp_info()
        data = tmp.data
        mmc.TXT_LIST.append(data)
        mmc.WYP_LIST.append(tmp)
    else: 
        print('List full!')


def draw_wypts()->None: 
    """
    Draws the waypoint list on the text space.

    Args: 
        None
    Returns: 
        None
    """
    for wyp in mmc.WYP_LIST: 
        rect(mmc.SCREEN, 
            mmc.WYP_COLOR, 
            wyp.ui_wyp)

# CONNECTIONS

def update_wyp_connection_list()->None:
    """
    This function updates the list of connections between waypoints. 

    Args: 
        wyp_a: The starting waypoint 
        wyp_b: The end waypoint

    Returns: 
        None
    """ 
    if len(mmc.WYP_LIST) > 1:
        # Get the waypoints only if the list is big enough 
        tmp = Connection(mmc.WYP_LIST[-2], mmc.WYP_LIST[-1])
        # Update the information of this connection by accessing the list
        tmp.set_connection_info()
        data = tmp.data
        mmc.TXT_LIST.append(data)        
        mmc.WYP_CONNECTION_LIST.append(tmp)



def draw_connections()->None:
    """
    This functions iterates through the connection list and draws the connection objects on the SCREEN display. It also draws the text for the connection info.

    Args: 
        None
    Returns: 
        None
    """ 
    for connection in mmc.WYP_CONNECTION_LIST: 
        line(mmc.SCREEN, 
             mmc.CONNECTION_COLOR, 
             connection.start.pixel_coords, 
             connection.finish.pixel_coords,
             5)
    

def draw_scene(sim_data : list)->None: 
    """
    This function draws the scene, including the main map, the fighter jet and the list of points

    Args: 
        sim_data: the simulation data 
    """

    # Display the reference image
    mmc.SCREEN.blit(scale(mmc.MANCHING_MAP, (mmc.CANVAS_X, mmc.CANVAS_Y)), (0, 0))

    # Convert the coordinates of the jet for every function that needs them
    lat, lon = get_coordinates(sim_data)

    # Draw fighter jet icon
    draw_fighter_jet(lat, lon, sim_data[5])

    # Render the trail
    draw_trail(lat, lon)

    draw_wypts()
    draw_connections()
    display_data()

    # Update the screen info
    display.update()


def moving_map_test_main()->None: 
    """
    Function to test the main functionality of the script without then simulator at hand. 

    Args: 
        None
    Returns: 
        None
    """

    init()
    setup_window_info()
    while mmc.RUNNING:
        for event in ev.get(): 
            if event.type == QUIT: 
                mmc.RUNNING = False 

            # Events with keys
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mmc.RUNNING = False
        # Check for events in program loop

            mouse_coordinates = get_pos()  

            if mouse_coordinates[0] <= mmc.MANCHING_MAP.get_width() and \
            mouse_coordinates[1] <= mmc.MANCHING_MAP.get_height() and \
            event.type == MOUSEBUTTONUP:
                mmc.TXT_CNT += 1
                update_wyp_list(mouse_coordinates) 
                update_wyp_connection_list()

        posi = bogus_data()
        draw_scene(posi)
    quit()

if __name__ == '__main__': 
    moving_map_test_main()
  
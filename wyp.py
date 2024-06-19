# Put the waypoints in a class
from pygame import Rect
import moving_map_conf as mmc

class Waypoint: 
    def __init__(self, x, y): 
        self.pixel_coords = (x, y)

        self.ui_wyp = Rect(x - 3, y - 3, 7, 7)
        self.data = str()
        self.index = mmc.WYP_CNT
        mmc.WYP_CNT += 1

        x = ((mmc.MAX_X[0] - mmc.MIN_X[0]) * (self.pixel_coords[0] - mmc.MIN_X[0])) / (mmc.MAX_X[1] - mmc.MIN_X[1]) + 11.0 + 20/60

        y = ((mmc.MAX_Y[0] - mmc.MIN_Y[0]) * (self.pixel_coords[1] - mmc.MIN_Y[0])) / (mmc.MAX_Y[1] - mmc.MIN_Y[1]) + 48.0 + 52/60

        self.gps_coords = (x, y)


    def set_wyp_info(self):
        self.data = f'WP{self.index} -> lat: {self.gps_coords[0]}     lon: {self.gps_coords[1]}'


class Connection: 
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish
        self.data = str()
        self.index = mmc.WYP_CONNECTION_CNT
        mmc.WYP_CONNECTION_CNT += 1

    def set_connection_info(self): 
        self.data = f'Start: WP{self.start.index}; End: WP{self.finish.index}'

        

# Put the waypoints in a class
from pygame import Rect
import moving_map_conf as mmc
from math import sin, asin, cos, acos, atan2, degrees, pow, sqrt, pi

class Waypoint: 
    def __init__(self, x, y): 
        self.pixel_coords = (x, y)

        self.ui_wyp = Rect(x - 3, y - 3, 10, 10)
        self.data = str()
        self.index = mmc.WYP_CNT
        mmc.WYP_CNT += 1

        lat = ((mmc.MAX_X[0] - mmc.MIN_X[0]) * (self.pixel_coords[0] - mmc.MIN_X[0])) / (mmc.MAX_X[1] - mmc.MIN_X[1]) + 11.0 + 20/60

        lon = ((mmc.MAX_Y[0] - mmc.MIN_Y[0]) * (self.pixel_coords[1] - mmc.MIN_Y[0])) / (mmc.MAX_Y[1] - mmc.MIN_Y[1]) + 48.0 + 52/60

        self.gps_coords = (lon, lat)

    def get_lat(self):
        return self.gps_coords[1] 
    
    def get_lon(self): 
        return self.gps_coords[0]

    def set_wyp_info(self):
        self.data = f'WP{self.index} -> lat: {str(self.get_lat())[:7]}{mmc.TXT_TAB}lon: {str(self.get_lon())[:7]}'


class Connection: 
    def __init__(self, start, finish):
        self.start = start
        self.finish = finish
        self.data = str()
        self.index = mmc.WYP_CONNECTION_CNT
        mmc.WYP_CONNECTION_CNT += 1

        # Data regarding assignment 3 
        self.tas = 100.0 * 1852.0 / 3600.0
        self.time = float
        self.verbose_time = str
        self.rwk = float
        self.distance = float

    def get_distance(self)->float:
        """
        This function retrieves the distance between the start and finish waypoints of the connection in NAUTICAL MILES

        Args: 
            None
        Returns: 
            distance in float
        """
        hypothenuse = sqrt(pow(self.start.get_lon() - self.finish.get_lon(), 2) + pow(self.start.get_lat() - self.finish.get_lat(), 2))

        self.distance = hypothenuse * 60


    def get_rwk(self)->None: 
        """
        This function returns the true course of the aricraft

        Args: 
            None
        Returns: 
            None
        """
        # THERE IS AN ERROR IN THE LOGIC; FIX IT!!!!!!        

        if (self.start.get_lon() - self.finish.get_lon()) == 0.0 and \
            (self.start.get_lat() - self.finish.get_lat()) > 0.0:
            self.rwk = 270.0
        
        elif (self.start.get_lon() - self.finish.get_lon()) == 0.0 and \
            (self.start.get_lat() - self.finish.get_lat()) < 0.0:
            self.rwk = 90.0

        elif (self.start.get_lon() - self.finish.get_lon()) > 0.0 and \
            (self.start.get_lat() - self.finish.get_lat()) == 0.0:
            self.rwk = 180.0

        elif (self.start.get_lon() - self.finish.get_lon()) < 0.0 and \
            (self.start.get_lat() - self.finish.get_lat()) == 0.0:
            self.rwk = 0.0

        dx = self.finish.get_lon() - self.start.get_lon()
        dy = self.finish.get_lat() - self.start.get_lat()

        rads = atan2(-dy, dx)
        rads %= 2*pi
        self.rwk = 360 - degrees(rads)
     


    def get_beta(self)->float:
        return mmc.WIND_DIRECTION - self.rwk * pi/180
    
    def get_luv(self)->float: 
        return asin(mmc.WIND_SPEED * sin(self.get_beta()/self.tas))
    
    def get_gamma(self)->float:
        return pi - (self.get_luv() + self.get_beta())
    
    def get_ground_speed(self)->float:
        return sqrt(pow(self.tas, 2) + pow(mmc.WIND_SPEED, 2)) - 2 * mmc.WIND_SPEED * self.tas * cos(self.get_gamma())
    
    def get_est_time(self)->float:
        self.time = abs(self.distance)/abs(self.get_ground_speed()) 

    def convert_time_to_verbose(self)->str:
        hours = self.time // 1
        minutes = ((self.time % 1) * 60/100) // 1
        seconds = ((self.time % 1) * 3600/100) // 1

        self.verbose_time = f'{hours}h {minutes}min {seconds}s'

    def set_connection_info(self): 
        # Set all the data
        self.get_rwk()
        self.get_distance()
        self.get_est_time()
        self.convert_time_to_verbose()

        self.data = f'Start: WP{self.start.index}; End: WP{self.finish.index}{mmc.TXT_TAB}'
        self.data += f'Distance: {str(self.distance)[:7]}NM{mmc.TXT_TAB}'
        self.data += f'RWK: {str(self.rwk)[:7]}°{mmc.TXT_TAB}'
        self.data += f'ETA: {str(self.time)[:7]}h'

        
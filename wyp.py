# Put the waypoints in a class
from pygame import Rect
import moving_map_conf as mmc
from math import sin, asin, cos, radians, atan2, degrees, pow, sqrt, pi

class Waypoint: 
    def __init__(self, x = 0.0, y = 0.0): 
        self.pixel_coords = (x, y)

        self.ui_wyp = Rect(x - 3, y - 3, 10, 10)
        self.data = ''
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
        self.gs = 100.0 * 1852.0 / 3600.0
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
        self.distance = sqrt(pow((self.start.get_lat() - self.finish.get_lat()) * 60.0, 2) + pow((self.start.get_lon()-self.finish.get_lon())*cos(radians(self.start.get_lat())) * 60.0, 2))
        return self.distance


    def get_rwk(self)->None: 
        """
        This function returns the true course of the aricraft

        Args: 
            None
        Returns: 
            None
        """
        # THERE IS AN ERROR IN THE LOGIC; FIX IT!!!!!!        
        if type(self.start) == None or type(self.finish) == None: 
            return None
        
        else:
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

            dx = (self.finish.get_lon() - self.start.get_lon()) * cos(radians((self.finish.get_lat() + self.start.get_lat())) / 2.0)
            dy = self.finish.get_lat() - self.start.get_lat()

            rads = atan2(-dy, dx)
            rads %= 2*pi
            self.rwk = 360 - degrees(rads)
            return self.rwk
     


    def get_beta(self)->float:
        return mmc.WIND_DIRECTION - self.rwk * pi/180
    
    def get_luv(self)->float: 
        return asin(mmc.WIND_SPEED * sin(self.get_beta()/self.gs))
    
    def get_gamma(self)->float:
        return pi - (self.get_luv() + self.get_beta())
    
    def get_ground_speed(self)->float:
        return sqrt(pow(self.gs, 2) + pow(mmc.WIND_SPEED, 2)) - 2 * mmc.WIND_SPEED * self.gs * cos(self.get_gamma())
    
    def get_est_time(self)->float:
        self.time = abs(self.distance * 1852)/abs(self.get_ground_speed()) 

    def convert_time_to_verbose(self)->str:
        self.verbose_time = '{0:02.0f}:{1:02.0f}'.format(*divmod(self.time, 60))

    def set_connection_info(self): 
        # Set all the data
        self.get_rwk()
        self.get_distance()
        self.get_est_time()
        self.convert_time_to_verbose()

        self.data = f'Start: WP{self.start.index}; End: WP{self.finish.index}{mmc.TXT_TAB}'
        self.data += f'Distance: {str(self.distance)[:7]}NM{mmc.TXT_TAB}'
        self.data += f'RWK: {str(self.rwk)[:7]}°{mmc.TXT_TAB}'
        self.data += f'ETA: {self.verbose_time}'

        

"""
New file for the autopilot functionality
"""
from wyp import Waypoint, Connection
import moving_map_conf as mmc 
import xpc

from math import pow, sqrt, sin, cos, radians, atan2, degrees, pi
import numpy as np


class Autopilot:
    def __init__(self): 
        self.current_wyp = Waypoint()
        self.wyp_flown_over_cnt = 0
        self.flown_over = False


    def vec_abs(self, vec):
        somma = 0
        for elem in vec:
            somma += pow(elem, 2)
        return sqrt(somma)


    def get_projection(self, jet_posi, connection : Connection)->float: 
        jet_posi = np.array([jet_posi[0], jet_posi[1]])
        a = np.array([connection.start.get_lon(), connection.start.get_lat()])
        b = np.array([connection.finish.get_lon(), connection.finish.get_lat()])

        tmp = jet_posi - a
        numerator = tmp[0]*b[1] - tmp[1]*b[0]
        denominator = self.vec_abs(b)

        return self.vec_abs(numerator) / denominator

    def get_dist_from_current_waypoint_in_km(self, jet_posi)->float:
        R = 6371.0
        d_lat = radians(self.current_wyp.get_lat() - jet_posi[1])
        d_lon = radians(self.current_wyp.get_lon() - jet_posi[0])

        a = sin(d_lat / 2) * sin(d_lat / 2) + cos(radians(jet_posi[1])) * sin(d_lon / 2) * sin(d_lon / 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c


        # return sqrt(pow((jet_posi[1] - self.current_wyp.get_lat()) * 60.0 * 1.852, 2) + pow((jet_posi[0]-self.current_wyp.get_lon())*cos(radians(jet_posi[1])) * 60.0 * 1.852, 2))


    def get_current_wyp(self): 
        """
        This function gets the current waypoint to fly towards, since there is no official function or decent logic to do that yet
        """
        
        # if the waypoint list contains elements: 
        if mmc.WYP_LIST:
            # if the waypoint list has only one element: 
            if len(mmc.WYP_LIST) < 2: 
                # return element with index 0
                self.current_wyp = mmc.WYP_LIST[0]

            # if waypoint list has more than one element: 
            else: 
                # check which waypoint you have already flown over and get the next waypoint in line by using self.wyp_flown_over_cnt as a reference
                try: 
                    print(f'wyp_flown_over_cnt = {self.wyp_flown_over_cnt}')
                    self.current_wyp = mmc.WYP_LIST[self.wyp_flown_over_cnt]
                except Exception as e:
                    if e == IndexError: 
                        print("Last waypoint of the list reached")
                    else: 
                        raise e

        else:
        # if no waypoint was marked yet, return nothing 
            print("No waypoint to fly towards yet")

    def get_rwk_from_jet(self, jet_posi)->float: 
        
        if (jet_posi[0] - self.current_wyp.get_lon()) == 0.0 and \
            (jet_posi[1] - self.current_wyp.get_lat()) > 0.0:
            self.rwk = 270.0
        
        elif (jet_posi[0] - self.current_wyp.get_lon()) == 0.0 and \
            (jet_posi[1] - self.current_wyp.get_lat()) < 0.0:
            self.rwk = 90.0

        elif (jet_posi[0] - self.current_wyp.get_lon()) > 0.0 and \
            (jet_posi[1] - self.current_wyp.get_lat()) == 0.0:
            self.rwk = 180.0

        elif (jet_posi[0] - self.current_wyp.get_lon()) < 0.0 and \
            (jet_posi[1] - self.current_wyp.get_lat()) == 0.0:
            self.rwk = 0.0

        dx = self.current_wyp.get_lon() - jet_posi[0]
        dx = (self.current_wyp.get_lon() - jet_posi[0]) * cos(radians((self.current_wyp.get_lat() + jet_posi[1])) / 2.0)
        dy = self.current_wyp.get_lat() - jet_posi[1]

        rads = atan2(-dy, dx)
        rads %= 2*pi
        rwk = 360 - degrees(rads)

        print(f'rwk = {rwk}')
        return rwk


    def flown_over_current_wyp(self, jet_posi)->bool:      
        """
        Checks if the fighter jet flew over the current waypoint
        
        Args: 
            jet_posi: simulation data

        Returns: 
            Either True or False
        """ 
        dist = self.get_dist_from_current_waypoint_in_km(jet_posi)
        print(f'dist = {dist}')

        if dist < mmc.PASSED_WYP_DISTANCE: 
            self.wyp_flown_over_cnt += 1


    def set_rwk_to_fly(self, jet_posi)->float:
        with xpc.XPlaneConnect() as client:
            self.get_current_wyp()
                  
            rwk = self.get_rwk_from_jet(jet_posi)
            print(f'rwk = {rwk}')
            
            client.sendDREF("sim/cockpit2/autopilot/heading_dial_deg_mag_pilot", rwk)

            if self.flown_over_current_wyp(jet_posi) and not self.flown_over: 
                self.wyp_flown_over_cnt += 1
                self.flown_over = True
            
            else: 
                self.flown_over = False






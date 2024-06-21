"""
New file for the autopilot functionality
"""
from wyp import Waypoint, Connection
import moving_map_conf as mmc 
import xpc

from math import pow, sqrt
import numpy as np

def vec_abs(vec):
    somma = 0
    for elem in vec:
        somma += pow(elem, 2)
    return sqrt(somma)


def get_projection(jet_posi, connection : Connection)->float: 
    jet_posi = np.array([jet_posi[0], jet_posi[1]])
    a = np.array([connection.start.get_lon(), connection.start.get_lat()])
    b = np.array([connection.finish.get_lon(), connection.finish.get_lat()])

    tmp = jet_posi - a
    numerator = tmp[0]*b[1] - tmp[1]*b[0]
    denominator = vec_abs(b)

    return numerator / denominator


def set_rwk_to_fly(jet_posi)->float: 
    """
    This function sets the trajectory or the simulated cessna to fly.

    Args: 
        None
    Returns: 
        correction: the angle the cessna needs to "correct" its trajectory towards while flying
    """

    '''
    if more than one waypoint was marked:
        create a connection between the jet and the latest connection finish point
        send a data ref to adjust the rwk to this connection
    
    ''' 
        

    with xpc.XPlaneConnect() as client:
        if len(mmc.WYP_CONNECTION_LIST) >= 1: 
            current_connection = Connection(Waypoint(jet_posi[0], jet_posi[1]), mmc.WYP_CONNECTION_LIST[mmc.CURRENT_CONNECTION_INDEX].finish)

            # How do I define a circle area?  
            if get_projection(jet_posi, mmc.WYP_CONNECTION_LIST[mmc.CURRENT_CONNECTION_INDEX]) < 50: 
                try:  
                    mmc.CURRENT_CONNECTION_INDEX += 1
                    client.sendDREF("sim/cockpit2/autopilot/heading_dial_deg_mag_pilot", mmc.WYP_CONNECTION_LIST[mmc.CURRENT_CONNECTION_INDEX].get_rwk())
                except: 
                    client.sendDREF("sim/cockpit2/autopilot/heading_dial_deg_mag_pilot", current_connection.get_rwk())
        
        else:
            if len(mmc.WYP_LIST) > 0: 
                current_connection = Connection(Waypoint(jet_posi[0], jet_posi[1]), mmc.WYP_LIST[0])
                client.sendDREF("sim/cockpit2/autopilot/heading_dial_deg_mag_pilot", current_connection.get_rwk())
            else:
                print('Flying without direction')

            

    # if that is not the case, do nothing

if __name__ == '__main__': 
    a = np.array([5, 6, 7])
    b = np.array([2, 3, 4])

    print(vec_abs(a))
    print(vec_abs(b))





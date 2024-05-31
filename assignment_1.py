import xpc

import socket
import time
import json

HOST = '127.0.0.1'
PORT_NR = 9000


def monitor():
    try: 
        processing_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('Created socket.')

        processing_server_socket.bind((HOST, PORT_NR))
        print('Socket was bound.')

        print(f'Listening for connection on port {PORT_NR}')
        processing_server_socket.listen(1)

        processing_client_socket, _ = processing_server_socket.accept()
        print('Connection accepted.')

    except Exception as e: 
        print(f'Exception occcured while binding the socket: {e}')

    with xpc.XPlaneConnect() as client:
        while True:
            posi = client.getPOSI()

            print("Loc: (%4f, %4f, %4f) Attitude (P %4f) (R %4f) (Y %4f)\n"
               % (posi[0], posi[1], posi[2], posi[3] , posi[4], posi[5]))
               
            autopilot_state = client.getDREFs("sim/cockpit/autopilot/autopilot_state")
            print("AP_State: %d", autopilot_state)

            try: 
                processing_client_socket.sendall(json.dumps(
                    {"simulatorData" : {
                        "lat" : posi[0], 
                        "lon" : posi[1],  
                        "yawAngle" : posi[5]
                    }}).encode() + b"\x17")
            
                print('Data succesfully sent to processing.')
            except Exception as e: 
                print(f'Exception occurred while sending the data to processing: {e}')

if __name__ == "__main__":


    dref1 = "sim/cockpit/autopilot/nav_steer_deg_mag"
    dref2 = "sim/cockpit/autopilot/autopilot_state"
        

    # Setup
    client = xpc.XPlaneConnect()

    # Execute
    client.sendDREF(dref1, 120.0)
    value = 512+16384
    client.sendDREF(dref2, value)
    # Cleanup
    client.close()
            
    monitor()
    
    # Screnshot either bayern atlas or AIP VFR Deutschland (ETSI Ingolstad Manching, you can find it on Moodle)
    # Put it in MS-paint 
    # Get the pixel values of your mapped point(s)
    # 
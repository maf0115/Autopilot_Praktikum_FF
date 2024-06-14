import xpc
from pygame import event, KEYDOWN, K_ESCAPE, QUIT, init
import ils

def monitor():
    # Initialize pygame as the first thing
    init()
    ils.setup_window_info()

    with xpc.XPlaneConnect() as client:
        ils.setup_window_info()
        while ils.RUNNING:
            for event_tmp in event.get(): 
                if event_tmp.type == QUIT: 
                    ils.RUNNING = False 

                # Events with keys
                elif event_tmp.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        ils.RUNNING = False

            posi = client.getPOSI()

            ils.draw_ils()
            ils.draw_horizontal_reference(posi)
            ils.draw_vertical_reference(posi) 
            ils.display.update()    
        quit()

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
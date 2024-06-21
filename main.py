import xpc
from pygame import init, quit
from pygame import event as ev
from pygame import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP
from pygame.mouse import get_pos
import moving_map_conf as mmc
import graphics
import autopilot


def monitor():
    # Initialize pygame as the first thing
    init()
    graphics.setup_window_info()

    with xpc.XPlaneConnect() as client:
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
                    graphics.update_wyp_list(mouse_coordinates) 
                    graphics.update_wyp_connection_list()

            posi = client.getPOSI()

            # print("Loc: (%4f, %4f, %4f) Attitude (P %4f) (R %4f) (Y %4f)\n"
               # % (posi[0], posi[1], posi[2], posi[3] , posi[4], posi[5]))
               
            autopilot_state = client.getDREFs("sim/cockpit/autopilot/autopilot_state")
            # print("AP_State: %d", autopilot_state)

            graphics.draw_scene(posi)
            autopilot.set_rwk_to_fly(posi)
            # Render the screen
        quit()



if __name__ == "__main__":


    dref1 = "sim/cockpit/autopilot/nav_steer_deg_mag"
    dref2 = "sim/cockpit/autopilot/autopilot_state"
        

    # Setup
    client = xpc.XPlaneConnect()

    # Execute
    client.sendDREF(dref1, 180.0)
    value = 512+16384
    client.sendDREF(dref2, value)
    # Cleanup
    client.close()
            
    monitor()
    
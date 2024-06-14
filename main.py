import xpc
import pygame
import graphics

def monitor():
    # Initialize pygame as the first thing
    pygame.init()
    graphics.setup_window_info()

    with xpc.XPlaneConnect() as client:
        while graphics.RUNNING:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    graphics.RUNNING = False 

                # Events with keys
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        graphics.RUNNING = False
            # Check for events in program loop

                mouse_coordinates = pygame.mouse.get_pos()  

                if mouse_coordinates[0] <= graphics.MANCHING_MAP.get_width() and \
                mouse_coordinates[1] <= graphics.MANCHING_MAP.get_height() and \
                event.type == pygame.MOUSEBUTTONUP:
                    graphics.update_wyp_list(mouse_coordinates) 

            posi = client.getPOSI()

            # print("Loc: (%4f, %4f, %4f) Attitude (P %4f) (R %4f) (Y %4f)\n"
               # % (posi[0], posi[1], posi[2], posi[3] , posi[4], posi[5]))
               
            autopilot_state = client.getDREFs("sim/cockpit/autopilot/autopilot_state")
            # print("AP_State: %d", autopilot_state)

            graphics.draw_scene(posi)
            # Render the screen
        pygame.quit()



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
    
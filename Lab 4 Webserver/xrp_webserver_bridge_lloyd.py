# Lab 4 - Webserver 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: Sept 29, 2025

# Goal:
# Build and run a webserver in bridge mode for remote control 

from XRPLib.defaults import * # Initializes board, motors, servo, and sensors
import time
import math
from machine import Timer

from Inverse_Kinematic_Algorithms import tst_algorithm
# tst_algorithm(final_position, current_heading)
global maneuver_state
global global_destination 
global initial_state
maneuver_state = False 
global_destination = []
initial_state = []

# optional initial_state 
def tst_waypoint(global_destination, initial_state=[0,0,0]):
    
    # Use the TST algorithm to create smooth paths between start point and target point
    # If no initial global state provided, TST will run effectively as local 
    
    # Check if robot is already maneuvering
    global maneuver_state 
    if maneuver_state == True:
        print("Error: wait for maneuver to complete")
        return 
    
    maneuver_state = True
    board.led_blink(2)
    
    x_prev = initial_state[0]
    y_prev = initial_state[1]
    theta_prev = initial_state[2] # theta measured from +x
    
    x = global_destination[0]
    y = global_destination[1]
    theta = global_destination[2]
    
    # Pass next target to TST algorithm
    relative_target_vector = [x-x_prev, y-y_prev, normalize_deg(theta-theta_prev)]
    tst_algorithm(relative_target_vector, current_heading=theta_prev) # move robot
    
    maneuver_state = False 
    print("Maneuver complete")
    print(maneuver_state)
    board.led_off()
    return 

def normalize_deg(deg):
    return (deg + 180.0) % 360.0 - 180.0
    
def point_input(msg):
    
    global maneuver_state
    global global_destination
    global initial_state
    if maneuver_state == True:
        print("Error: wait for maneuver to complete")
        return
    
    # msg must be either a string 3 numbers long or 6 numbers long
    combined_vector = eval(msg)
    global_destination = combined_vector[0:3]
    initial_state = [0,0,0]
    if len(combined_vector) == 6:
        initial_state = combined_vector[3:6]
    print(f"Received message: {msg}")
    print(f"Destination: {global_destination}")
    print(f"Initial: {initial_state}")
    return


def log_maneuver_state():
    # This function is called every second to update the data on the webserver
    global maneuver_state
    global global_destination 
    webserver.log_data("Maneuver State", maneuver_state)
    webserver.log_data("Destination Vector", global_destination)
    
def maneuver_state_reset():
    global maneuver_state
    maneuver_state = False
    return

# PROGRAM START
webserver = Webserver.get_default_webserver() # initialize webserver object

# Binding functions to the arrow buttons
webserver.registerForwardButton(lambda: drivetrain.set_effort(0.5, 0.5))
webserver.registerLeftButton(lambda: drivetrain.set_effort(-0.5, 0.5))
webserver.registerRightButton(lambda: drivetrain.set_effort(0.5, -0.5))
webserver.registerBackwardButton(lambda: drivetrain.set_effort(-0.5, -0.5))
webserver.registerStopButton(lambda: drivetrain.set_effort(0, 0))

# Binding functions to custom buttons
webserver.add_button("Close Server", lambda: webserver.stop_server())
webserver.add_button("Blink", lambda: board.led_blink(2))
webserver.add_button("LED Off", lambda: board.led_off())

webserver.add_button("TST Drive", lambda: tst_waypoint(global_destination, initial_state))
webserver.add_button("Reset Maneuver State to False", lambda: maneuver_state_reset())
webserver.add_field("Input TST vectors [x,y,theta,x0,y0,theta0]", lambda msg: point_input(msg), "[x,y,theta,x0,y0,theta0]")

maneuver_state = False # initialize state 

timer = Timer(-1)
timer.init(period=250, mode=Timer.PERIODIC, callback=lambda t: log_maneuver_state())


# Run server last 
webserver.connect_to_network() # use secrets.json file for home wifi and password
webserver.start_server()


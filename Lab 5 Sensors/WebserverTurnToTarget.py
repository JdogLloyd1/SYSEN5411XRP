# Lab 5 - Sensors TST 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: October 5, 2025

# Goal:
# Build a TST algorithm that checks for obstacles before driving

from XRPLib.defaults import *
import time
import math
from machine import Timer
import os

global maneuver_state
global global_destination 
global initial_state
maneuver_state = False 
global_destination = []
initial_state = []



# Define New TST algorithm with obstacle check
def tst_algorithm_with_obstacle_check(final_position, current_heading):

    # Coordinate system: +x right, +y forward, theta CCW from +x
    # Initial condition: (0, 0, 0) Relative coordinate system
    success = True
    x_final = final_position[0]
    y_final = final_position[1]
    theta_final = final_position[2]   
    
    # 1. Turn to face the target
    alpha_wrtx = math.degrees(math.atan2(y_final, x_final)) # degrees relative to +x
    alpha_turn = (alpha_wrtx - current_heading +180) % 360 - 180 # delta turn, normalize to [-180, 180]
    drivetrain.turn(turn_degrees=alpha_turn) 
    
    # 2. Straight to target
    distance_target = math.sqrt(x_final**2 + y_final**2)
    # Take 5 readings after alpha turn and take median
    readings = []
    for i in range(5):
        readings.append(rangefinder.distance())
    median_reading = sorted(readings)[2]

    # If median reading is less than target distance to drive, then exit
    if median_reading < distance_target:
        print("Obstacle detected, exiting TST")
        drivetrain.set_effort(0, 0)
        board.set_rgb_led(255, 0, 0)
        time.sleep(0.5)
        board.set_rgb_led(0, 0, 0)
        time.sleep(0.5)
        board.set_rgb_led(255, 0, 0)
        time.sleep(0.5)
        board.set_rgb_led(0, 0, 0)
        time.sleep(0.5)
        board.set_rgb_led(255, 0, 0)
        time.sleep(0.5)
        board.set_rgb_led(0, 0, 0)
        time.sleep(0.5)
        success = False
        with open('obstacle_log.txt', 'a') as f:
            f.write("Obstacle detected, exiting TST\n")
            f.write(f"Median reading: {median_reading}\n")
            f.write(f"Distance Target: {distance_target}\n")
        return False
    # If no obstacles, then proceed with TST
    print("No obstacles detected, proceeding with TST")
    drivetrain.straight(distance=distance_target)
    
    # 3. Turn to final heading
    beta_turn = (theta_final - alpha_turn +180) % 360 - 180 # normalize to [-180, 180]
    drivetrain.turn(turn_degrees=beta_turn)
    
    return success

# Define waypoint movement function
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
    maneuver_succeeded = tst_algorithm_with_obstacle_check(relative_target_vector, current_heading=theta_prev)
    maneuver_state = False
    if maneuver_succeeded == False:
        print('Maneuver failed')
        print(maneuver_state)    
        board.led_off()
        return
    else:
        print("Maneuver complete")
        print(maneuver_state)
        board.led_off()
        return 


# Helper function to normalize degrees over -pi to pi
def normalize_deg(deg):
    return (deg + 180.0) % 360.0 - 180.0
    
# Webserver helper functions
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

# Instantiate Webserver
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


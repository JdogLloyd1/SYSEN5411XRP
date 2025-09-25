# Lab 3 - Waypoints
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: Sept 24, 2025


# Goal:
# Demonstrate waypoint navigation algorithm

from XRPLib.defaults import * # Initializes board, motors, servo, and sensors
import time
import math

from Inverse_Kinematic_Algorithms import tst_algorithm
# tst_algorithm(final_position, current_heading)
from circle_algorithm import *
# normalize_deg(deg)
# generate_circle_path(n_points, radius_cm, closed=True, ccw=True)


# define main algorithm
def waypoint_nav(circle_points, circle_radius):
    
    # Use the TST algorithm combined with generate_circle_path
    # to create smooth paths between start point and target point
    
    # Create circle path
    # theta is generated wrt +x axis 
    waypoints = generate_circle_path(circle_points, circle_radius,
                                     closed=True, ccw=True)
    
    # Feed circle path step by step to TST algorithm
    distance_traveled = 0 # centimeters, running tally of commanded distance
    x_prev = 0
    y_prev = 0
    theta_prev = 0 # initial condition of robot facing right here, theta measured from +x
    current_location = [x_prev, y_prev, theta_prev] # initial condition of robot 
    del(waypoints[0]) # remove first (0,0,0) point to send robot straight to next corner
    relative_points = []
    for x, y, theta in waypoints:
        # Pass next target to TST algorithm
        absolute_target_vector = [x, y, theta] # absolute coordinates
        relative_target_vector = [x-x_prev, y-y_prev, normalize_deg(theta-theta_prev)]
        relative_points.append(relative_target_vector)
        tst_algorithm(relative_target_vector, current_heading=theta_prev) # move robot
        
        # Delta distance and update counter
        d_segment = math.sqrt((x-x_prev)**2 + (y-y_prev)**2)
        distance_traveled = distance_traveled + d_segment 
        
        # Set n-1 point
        x_prev = x
        y_prev = y
        theta_prev = theta
        current_location = absolute_target_vector # update position of robot 
    
    return waypoints, distance_traveled, relative_points
    

# PROGRAM START

# Blink LED to signal successful boot and program load
board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()

# Define number of circle points
N_circle = 4
# N_circle = 8
# N_circle = 12

# Define circle radius
radius = 50 # cm

# Drive
# Initial condition: (0,0,-90) at base of circle pointing to the right 
print("Ready to run Waypoint Algorithm")
board.wait_for_button() # wait to run code until USER button is pressed
time.sleep(1)
# exportWaypoints, commandedDistanceTraveled, relative_waypoints = waypoint_nav(N_circle, radius)
exportWaypoints, commandedDistanceTraveled, relative_waypoints = waypoint_nav(N_circle, radius)

with open('waypoint_log_N' + str(N_circle) + '_points.txt', 'w') as f:
    f.write("Commanded Distance Traveled: \n")
    f.write(f'{commandedDistanceTraveled}\n')
    f.write("Commanded Global Waypoints: \n")
    f.write(f'{exportWaypoints}\n')
    f.write("Relative Waypoints: \n")
    f.write(f'{relative_waypoints}\n')
    
# Set board light to green to signify code complete
board.set_rgb_led(0,255,0) # range 0-255 for each r,g,b








# Lab 3 - Inverse Kinematic Algorithms
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: Sept 21, 2025

# Goal:
# Command differential drive robot to follow 3 or 4 step inverse kinematics approach
# to go from (0,0) to designated (x,y,Theta)

import time
import math

    
def tst_algorithm_relative(final_position, current_position):
    
    # Coordinate system: +x right, +y forward, theta CCW from +x
    # Initial condition: (0, 0, 0)

    x_final = final_position[0]
    y_final = final_position[1]
    theta_final = final_position[2]   
    
    x_current = current_position[0]
    y_current = current_position[1]
    theta_current = current_position[2]

    x_delta = x_final - x_current
    y_delta = y_final - y_current
    theta_delta = theta_final - theta_current

    # 1. Turn to face the target
    alpha_wrtx = math.degrees(math.atan2(y_delta, x_delta)) # degrees relative to +x
    alpha_turn = (alpha_wrtx - 90 +180) % 360 - 180 # transform to wrt +y, normalize to [-180, 180]
    
    # 2. Straight to target
    distance_target = math.sqrt(x_delta**2 + y_delta**2)

    # 3. Turn to final heading
    beta_turn = (theta_final - alpha_turn +180) % 360 - 180 # normalize to [-180, 180]
    
# Lab 3 - Inverse Kinematic Algorithms
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: Sept 21, 2025

# Goal:
# Command differential drive robot to follow 3 or 4 step inverse kinematics approach
# to go from (0,0) to designated (x,y,Theta)

from XRPLib.defaults import * # Initializes board, motors, servo, and sensors
import time
import math

# main function definitions
def stst_algorithm(final_position):
    
    start_clock = time.time() # start timer
    
    # Coordinate system: +x right, +y forward, theta CCW from +x
    # Initial condition: (0, 0, 0)
    
    x_final = final_position[0]
    y_final = final_position[1]
    theta_final = final_position[2]
    
    x_0 = 0
    y_0 = 0
    theta_0 = 0
    
    # 1. First straight in y
    x_1 = x_0
    y_1 = y_0 + y_final
    theta_1 = theta_0
    drivetrain.straight(distance=y_1-y_0)
        
    # 2. Intermediate turn
    x_2 = x_1
    y_2 = y_1
    if x_final > 0:
        theta_2 = theta_1 - 90
    else: 
        if x_final < 0:
            theta_2 = theta_1 + 90
        else: # x_final = 0
            theta_2 = theta_1
    drivetrain.turn(turn_degrees=theta_2-theta_1)
    
    # 3. Second straight in x
    x_3 = x_2 + x_final
    y_3 = y_2
    theta_3 = theta_2
    drivetrain.straight(distance=x_3-x_2)
    
    # 4. Final turn
    x_4 = 0
    y_4 = y_3
    theta_4 = theta_final
    drivetrain.turn(turn_degrees=theta_4-theta_3)
          
    
    end_clock = time.time() # end timer
    runtime = end_clock - start_clock
    return runtime
    
def tst_algorithm(final_position):
    
    start_clock = time.time() # start timer
    
    # Coordinate system: +x right, +y forward, theta CCW from +x
    # Initial condition: (0, 0, 0)

    x_final = final_position[0]
    y_final = final_position[1]
    theta_final = final_position[2]   
    
    # 1. Turn to face the target
    alpha_wrtx = math.degrees(math.atan2(y_final, x_final)) # degrees relative to +x
    alpha_turn = (alpha_wrtx - 90 +180) % 360 - 180 # transform to wrt +y, normalize to [-180, 180]
    drivetrain.turn(turn_degrees=alpha_turn)
    
    # 2. Straight to target
    distance_target = math.sqrt(x_final**2 + y_final**2)
    drivetrain.straight(distance=distance_target)
    
    # 3. Turn to final heading
    beta_turn = (theta_final - alpha_turn +180) % 360 - 180 # normalize to [-180, 180]
    drivetrain.turn(turn_degrees=beta_turn)
    
    
    end_clock = time.time() # end timer
    runtime = end_clock - start_clock
    return runtime
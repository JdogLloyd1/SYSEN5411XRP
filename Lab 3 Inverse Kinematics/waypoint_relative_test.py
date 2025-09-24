# test

import time
import math

from circle_algorithm import *
# normalize_deg(deg)
# generate_circle_path(n_points, radius_cm, closed=True, ccw=True)

# normalize_deg(deg)
# generate_circle_path(n_points, radius_cm, closed=True, ccw=True)

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
    theta_delta = (theta_final - theta_current +180) % 360 - 180
    print("Delta movement:")
    print(x_delta, y_delta, theta_delta)

    # 1. Turn to face the target
    alpha = math.degrees(math.atan2(x_delta, y_delta)) # degrees 
    alpha_turn = (alpha +180) % 360 - 180 # normalize to [-180, 180]
    print("Turn angle 1: ", alpha_turn)

    # 2. Straight to target
    distance_target = math.sqrt(x_delta**2 + y_delta**2)
    print("Distance: ", distance_target)

    # 3. Turn to final heading
    beta_turn = (theta_delta - alpha_turn +180) % 360 - 180 # normalize to [-180, 180]
    print("Turn angle 2: ", beta_turn)


circle_points = 4
circle_radius = 10 # cm
    
# Use the TST algorithm combined with generate_circle_path
# to create smooth paths between start point and target point

# Create circle path
waypoints = generate_circle_path(circle_points, circle_radius,
                                    closed=True, ccw=True)
print(waypoints)
print() 

# Feed circle path step by step to TST algorithm
distance_traveled = 0 # centimeters, running tally of commanded distance
x_prev = 0
y_prev = 0
theta_prev = -90 # initial condition of robot facing right here, theta measured from +y
print("Initial position wrt +y): ")
current_location = [x_prev, y_prev, theta_prev] # initial condition of robot facing +y
print(current_location)

del(waypoints[0]) # remove first point, already at (0,0)
for x, y, theta in waypoints:
    # Pass next target to TST algorithm
    absolute_target_vector = [x, y, normalize_deg(theta-90)] # absolute coordinates, theta converted to +y
    tst_algorithm_relative(absolute_target_vector, current_location) # move robot
    
    # Delta distance and update counter
    d_segment = math.sqrt((x-x_prev)**2 + (y-y_prev)**2)
    distance_traveled = distance_traveled + d_segment
    
    # Set n-1 point
    x_prev = x
    y_prev = y
    theta_prev = theta-90 # continue converting to +y reference
    current_location = absolute_target_vector # update position of robot theta wrt +y
    print("New position wrt +y): ")
    print(current_location)
    print()

print("Total distance traveled: ", distance_traveled)



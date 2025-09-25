# test

import time
import math

from circle_algorithm import *
# normalize_deg(deg)
# generate_circle_path(n_points, radius_cm, closed=True, ccw=True)

# normalize_deg(deg)
# generate_circle_path(n_points, radius_cm, closed=True, ccw=True)

def tst_algorithm(final_position, current_heading):
    
    # Coordinate system: +x right, +y forward, theta CCW from +x
    # Initial condition: (0, 0, 0)

    x_final = final_position[0]
    y_final = final_position[1]
    theta_final = final_position[2]   


    # 1. Turn to face the target
    alpha_wrtx = math.degrees(math.atan2(y_final, x_final)) # degrees relative to +x
    alpha_norm = (alpha_wrtx - current_heading +180) % 360 - 180 # normalize to [-180, 180]
    print("Turn angle 1: ", alpha_norm)

    # 2. Straight to target
    distance_target = math.sqrt(x_final**2 + y_final**2)
    print("Distance: ", distance_target)

    # 3. Turn to final heading
    beta_turn = (theta_final - alpha_norm +180) % 360 - 180 # normalize to [-180, 180]
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
theta_prev = 0 # initial condition of robot facing right here, theta measured from +x
print("Initial position wrt +x): ")
current_location = [x_prev, y_prev, theta_prev] # initial condition 
print(current_location)
relative_points = [] # list of relative points for debugging
del(waypoints[0]) # remove first point, already at (0,0)
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
    current_location = absolute_target_vector # update position of robot theta wrt +y
    print("New position wrt +y: ")
    print(current_location)
    print()

print("Total distance traveled: ", distance_traveled)
print("Relative points: ", relative_points)


# Lab 3 - Inverse Kinematics
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: Sept 21, 2025

# Goal:
# Command differential drive robot to follow 3 or 4 step inverse kinematics approach
# to go from (0,0) to designated (x,y,Theta)

from XRPLib.defaults import * # Initializes board, motors, servo, and sensors
import time
import math

from Inverse_Kinematic_Algorithms import *
# stst_algorithm(final_position)
# tst_algorithm(final_position, current_heading)
    
# PROGRAM START

# Blink LED to signal successful boot and program load
board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()

# Define end position
# [x, y, theta]
# target_vector = [0, 0, 195]
target_vector = [25, 15, 90]
# target_vector = [40, -15, -45]

# Drive
print("Ready to run STST")
board.wait_for_button() # wait to run code until USER button is pressed
time.sleep(1)
stst_timer = stst_algorithm(target_vector)

# PHYSICALLY RESET ROBOT TO (0,0,0)

# Blink LED to signal ready for second algorithm
board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()

print("Ready to run TST")
board.wait_for_button() # wait to run code until USER button is pressed
time.sleep(1)
tst_timer = tst_algorithm(target_vector, current_heading=0)

board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()


with open('timer_log '+ str(target_vector) +'.txt', "w") as f:
    f.write("Target Vector: \n")
    f.write(f"{target_vector}\n")
    f.write("STST Timer: \n")
    f.write(f"{stst_timer}\n")
    f.write("TST Timer: \n")
    f.write(f"{tst_timer}\n")

# Set board light to green to signify code complete
board.set_rgb_led(0,255,0) # range 0-255 for each r,g,b

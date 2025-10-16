# Lab 6 - PID Control 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: October 16, 2025

# Goal:
# PID control of XRP robot using ultrasonic sensor
# facing forwards to maintain a fixed distance from a wall. 

from XRPLib.defaults import *
from XRPLib.pid import *
import time
import math
from machine import Timer
import os

# Define loop function
def pid_wall_distance(target, gains):
    
    # Target is in centimeters for ultrasonic sensor
    # Unpack the control gains 
    kp = gains[0]
    ki = gains[1]
    kd = gains[2]
    
    # Initialize PID controller from XRPLib
    controller = PID(kp, ki, kd, max_output=0.6)
    
    while board.is_button_pressed() == False: 
        error = target - rangefinder.distance()
        effort = controller.update(error)
        drivetrain.set_effort(-effort, -effort)
        time.sleep(0.01)
    
    drivetrain.set_effort(0,0) # reset motors
    # Blink LED to signal program completion 
    board.led_blink(5) # blink at 5 Hz
    time.sleep(2)
    board.led_off()
    print("Controller Run Ended")
    return 


# PROGRAM START

drivetrain.set_effort(0,0) # reset motors
# Blink LED to signal successful boot and program load
board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()

print("Ready to run")
board.wait_for_button() # wait to run code until USER button is pressed
time.sleep(1)

# Run controller
wall_distance_target = 10 # centimeters
control_gains = [0.25, 0.06, 0.04]
pid_wall_distance(wall_distance_target, control_gains)

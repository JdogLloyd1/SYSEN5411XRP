# Lab 8 - 1D Kalman Filter
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: November 8, 2025

# Goal:
# 15 Second PID Data Collection Run for Offline Fusion

from XRPLib.defaults import *
import time
import math
from machine import Timer
import os
from XRPLib.pid import PID

# Define loop function
def pid_drive_15sec():
    
    max_time = 15*1000 # milliseconds of runtime
    PIDCONST = [0.2, 0.4, 0.02]
    
    controller = PID(kp=PIDCONST[0], ki=PIDCONST[1], kd=PIDCONST[2], max_output=.9)
    target = 25 # cm distance from wall 
    
    f = open("data.csv", "w")
    start_time = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start_time) < max_time:
        error = target - rangefinder.distance()
        effort = controller.update(error)
        drivetrain.set_effort(-effort, -effort)  
        left_encoder = drivetrain.get_left_encoder_position()
        right_encoder = drivetrain.get_right_encoder_position()
        
        f.write(f"{time.ticks_diff(time.ticks_ms(), start_time)/1000:.3f},{left_encoder}, {right_encoder}, {error}, {effort}\n")
        time.sleep(0.0001)
        
    drivetrain.stop()
    print("Controller Run Ended")
    f.close()
    
    
##################################
# START RUNTIME CODE
drivetrain.set_effort(0,0) # reset motors
# Blink LED to signal successful boot and program load
board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()

print("Ready to run")
board.wait_for_button() # wait to run code until USER button is pressed
time.sleep(1)

print("Running")
pid_drive_15sec()


board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()

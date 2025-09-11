# Lab 1 - XRP Robot Setup 
# SYSEN 5411 Fall 2026
# Author: Jonathan Lloyd
# Last update: Sept 8, 2025

# Goal:
# Test functionality of robot sensors and motors on startup
# Hardware to test:
# - ultrasonic sensor
# - reflectance sensor
# - wheel motors
# - servo motor

# Robot initial condition:
# User first set up a min. 6 inch long strip of high contrast tape
# on the test surface.
# Set the robot with reflectance sensor mounted facing down,
# on top of the line.
# Servo can be in any orientation.

from XRPLib.defaults import *
# Initializes board, motors, servo, and sensors
import time


# main function definition
def lloyd_ivp():
    # print startup
    print("Running Boot Check")
    
    # LED test: flash STAT LED @ 2 Hz
    print("flash")
    board.led_blink(2)
    print("green")
    board.set_rgb_led(0,255,0) # range 0-255 for each r,g,b
    
    time.sleep(5)
    
    print("lights off")
    board.led_off() # stop blink
    board.set_rgb_led(0,0,0)
    print("Blink Complete")
    
    time.sleep(1)
    
    # line follow test for 5 seconds
    line_track(1)
    
    time.sleep(1)
    
    # temperature sensor test
    print("Board temperature in degrees Celsius")
    print(imu.temperature())
    
    time.sleep(1)
    
    # servo actuation test
    print("Move servo to face lever arm fully forwards")
    # angle options [0, 200]
    servo_one.set_angle(200)
    
    time.sleep(1)
    
    print("XRP Initialization Complete")
    
    
# line follow function from example code 
def line_track(runtime):
    base_effort = 0.6
    KP = 0.6
    start_time = time.time()
    while time.time() - start_time < runtime:
        # You always want to take the difference of the sensors because the raw value isn't always consistent.
        error = reflectance.get_left() - reflectance.get_right()
        # print(error)
        drivetrain.set_effort(base_effort - error * KP, base_effort + error * KP)
        time.sleep(0.01)
        
    drivetrain.set_effort(0, 0)

# run program
lloyd_ivp()

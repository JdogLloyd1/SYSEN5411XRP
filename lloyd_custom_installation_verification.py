# Lab 1 - XRP Robot Setup 
# SYSEN 5411 Fall 2026
# Author: Jonathan Lloyd
# Last update: Sept 3, 2025

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
    
    # line follow test
    
    
    # ultrasonic sensor test
    
    
    # servo actuation test
    
    
# define board
board = Board.get_default_board()

# run program
lloyd_ivp()

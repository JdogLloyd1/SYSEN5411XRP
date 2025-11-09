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

# Define loop function


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



board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()

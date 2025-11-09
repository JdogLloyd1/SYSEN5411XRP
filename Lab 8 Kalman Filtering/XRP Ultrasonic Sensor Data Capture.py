# Lab 8 - 1D Kalman Filter
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: November 8, 2025

# Goal:
# Measure mean and standard deviation for
# XRP ultrasonic sensor to characterize sensor noise

from XRPLib.defaults import *
import time
import math
from machine import Timer
import os

# Define main function
def gather_and_compute(tapeMeasureDistance):
    
    # List to store ultrasonic rangefinder readings
    measurementCount = 1000
    rangefinderLog = [None] * measurementCount
    
    # Gather 1000 readings
    for i in range(0,measurementCount):
        rangefinderLog[i] = rangefinder.distance()
        time.sleep(0.01)
    
    # Calculate mean and variance 
    mu = sum(rangefinderLog) / len(rangefinderLog)
    variance = sum((x-mu) ** 2 for x in rangefinderLog) / len(rangefinderLog)
    
    # Export to file
    file = open('Lab8UltrasonicData.txt', 'a') # Opens the file in append mode
    file.write(f"\nNominal distance = {tapeMeasureDistance} cm")
    file.write(f"\nMu = {mu} cm") # Appends new data
    file.write(f"\nVar = {variance} cm")
    file.write("\n")
    file.close() # Closes the file
    print("Export Complete")
    
    board.led_blink(5) # blink at 5 Hz
    time.sleep(2)
    board.led_off()
    
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

distance_set = [8, 23, 61, 102, 170]
file = open('Lab8UltrasonicData.txt', 'w') # Opens the file in append mode
file.write("Run Start \n") # Appends new data
file.close() # Closes the file

for i in range(len(distance_set)):
    print("Running")
    gather_and_compute(distance_set[i])
    board.wait_for_button() # wait to run code until USER button is pressed
    time.sleep(1)

board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()
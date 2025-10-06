# Lab 5 - Sensors TST 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: October 5, 2025

# Goal:
# Build a 360 degree range map around the XRP

from XRPLib.defaults import *
import time
import math
from machine import Timer
import os

# Define function
def three_sixty_lidar():
    # Spin robot for 360 degrees
    # Every 15 degrees, pull range data from ultrasonic sensor
    degree_list = []
    range_list = []
    range_sample = []
    for i in range(24): # 15 degrees * 24 = 360 degrees
        degree = i * 15
        for j in range(5): # 5 samples to average
            range = rangefinder.distance()
            range_sample.append(range)
            time.sleep(0.1)
        
        range_avg = sum(range_sample) / len(range_sample) # average 
        if range_avg >= 60000: # Error catch
            range_avg = -1
            
        degree_list.append(degree)
        range_list.append(range_avg)
        range_sample = [] # reset sample list
        
        drivetrain.turn(turn_degrees=15) # turn 15 degrees
        time.sleep(0.1)

    # Log degree and range to a list
    return degree_list, range_list

# Save lists to CSV
def save_to_csv(degree_list, range_list):
    with open('scan.csv', 'w') as f:
        f.write('Degree,Range\n') # header
        
        for degree, range in zip(degree_list, range_list):
            f.write(f"{degree},{range}\n")

# PROGRAM START
degreelist, rangelist = three_sixty_lidar()
save_to_csv(degreelist, rangelist)

# Postprocess polar plot offline
# Lab 7 - IMU and Signal Processing 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: October 26, 2025

# Goal:
# Task B1 - demonstrate gyroscope drift without offsets

from XRPLib.defaults import *
import time
import math
from machine import Timer
import os

# Define loop function
def data_recording():
    
    # Record 30 seconds of data at 200 Hz
    # - accelerometer data
    # - gyro data 
    # Log to CSV
    
    fs = 200 # Hz
    dt = 1.0 / fs
    with open("B1_gyro_log.csv", "w") as f:
        f.write("t_ms,ax_mg,ay_mg,az_mg,roll_acc_deg,pitch_acc_deg,gyro_int_roll,gyro_int_pitch\n")
        t0 = time.ticks_ms()
        
        for _ in range(200*30): # 30 sec @ 200 Hz
            ax, ay, az = imu.get_acc_rates()
            roll_acc, pitch_acc = compute_roll_pitch(ax, ay, az)
            gyro_int_roll = imu.get_roll() # already in deg
            gyro_int_pitch = imu.get_pitch() # already in deg           
            t_ms = time.ticks_diff(time.ticks_ms(), t0)
            f.write("%d,%d,%d,%d,%.3f,%.3f,%.3f,%.3f\n" % (t_ms, ax, ay, az, roll_acc,
            pitch_acc, gyro_int_roll, gyro_int_pitch))
            time.sleep(dt)
            
        print("Saved B1_gyro_log.csv")
    
    
def compute_roll_pitch(ax_mg, ay_mg, az_mg):
    
    # Helper: compute roll/pitch from accelerometer (mg→g, radians→degrees)
    
    ax = ax_mg / 1000.0
    ay = ay_mg / 1000.0
    az = az_mg / 1000.0
    
    roll = math.degrees(math.atan2(ay, az))
    pitch = math.degrees(math.atan2(-ax, math.sqrt(ay*ay + az*az)))
    
    return roll, pitch

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
imu.calibrate()
imu.gyro_offsets[0] = 0
imu.gyro_offsets[1] = 0
imu.gyro_offsets[2] = 0

data_recording()

board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()
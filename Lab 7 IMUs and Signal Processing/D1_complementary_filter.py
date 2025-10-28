# Lab 7 - IMU and Signal Processing 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: October 26, 2025

# Goal:
# Task D1 - Complementary Filter for roll and pitch

from XRPLib.defaults import *
import time
import math
from machine import Timer
import os

# Define loop function
def data_recording(alpha):
    
    # Record 30 seconds of data at 200 Hz
    # - raw axis
    # - filtered axis
    # Log to CSV
        
    fs = 200 # Hz
    dt = 1.0 / fs
    
    # Initial estimates
    roll_est = imu.get_roll()
    pitch_est = imu.get_pitch()
    
    with open(f"D1_complementary_{alpha}.csv", "w") as f:
        
        f.write("t_ms,roll_acc,roll_comp,pitch_acc,pitch_comp\n")
        t0 = time.ticks_ms()
                      
        for _ in range(200*30):
            # Read both sensors together (mg, mdps)
            (ax, ay, az), (gx, gy, gz) = imu.get_acc_gyro_rates()
            
            # Accelerometer angles
            ax_g, ay_g, az_g = ax/1000.0, ay/1000.0, az/1000.0
            roll_acc = math.degrees(math.atan2(ay_g, az_g))
            pitch_acc = math.degrees(math.atan2(-ax_g, math.sqrt(ay_g*ay_g +
            az_g*az_g)))
            
            # Gyro rates (deg/s)
            gx_dps = gx / 1000.0 # X → pitch
            gy_dps = gy / 1000.0 # Y → roll
            
            # Predict step (integrate gyro)
            roll_pred = roll_est + gy_dps * dt
            pitch_pred = pitch_est + gx_dps * dt
            
            # Correct step (blend with accel)
            roll_est = alpha * roll_pred + (1.0 - alpha) * roll_acc
            pitch_est = alpha * pitch_pred + (1.0 - alpha) * pitch_acc
            
            # Write data to CSV
            t_ms = time.ticks_diff(time.ticks_ms(), t0)
            f.write("%d,%.3f,%.3f,%.3f,%.3f\n" % (t_ms, roll_acc, roll_est,
            pitch_acc, pitch_est))
            time.sleep(dt)
            
        print("Saved D1 csv file")
    

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
alpha = 0.995 # try 0.90, 0.98, 0.995

data_recording(alpha)

board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()

# Lab 7 - IMU and Signal Processing 
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: October 26, 2025

# Goal:
# Task C1 - Low Pass Filter of raw axis 

from XRPLib.defaults import *
import time
import math
from machine import Timer
import os

class LowPass:
    def __init__(self, alpha, y0=0.0):
        self.a = alpha
        self.y = y0
        self.init = True
    def step(self, x):
        if self.init:
            self.y = x # start from first sample
            self.init = False
        else:
            self.y = self.a * self.y + (1.0 - self.a) *x
        return self.y


# Define loop function
def data_recording(alpha):
    
    # Record 30 seconds of data at 200 Hz
    # - raw axis
    # - filtered axis
    # Log to CSV
    
    lp = LowPass(alpha)
    
    fs = 200 # Hz
    dt = 1.0 / fs
    with open(f"C1_axis_alpha_{alpha}.csv", "w") as f:
        f.write("t_ms,ax_g,ax_lpf_g\n")
        t0 = time.ticks_ms()
        
        for _ in range(200*30): # 30 sec @ 200 Hz
            ax, ay, az = imu.get_acc_rates() # in mg
            ax_lpf = lp.step(ax)
            ax = ax / 1000.0 # convert mgs to gs
            ax_lpf = ax_lpf / 1000.0 # convert mgs to gs
            t_ms = time.ticks_diff(time.ticks_ms(), t0)
            f.write("%d,%.3f,%.3f\n" % (t_ms, ax, ax_lpf))
            time.sleep(dt)
            
        print("Saved C1 csv file")
    

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
alpha = 0.9 # try 0.1, 0.5, 0.9

data_recording(alpha)

board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()

# Lab 2 Part 2 - Forward Kinematics Measurement vs Prediction
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: Sept 14, 2025

# Goal:
# Compare predicted robot performance to actual movement commands

from XRPLib.defaults import * # Initializes board, motors, servo, and sensors
import time
import math

# main function definition
def motion_sequence_one():
    
    # Robot initial condition - reset encoders to zero
    drivetrain.stop()
    drivetrain.reset_encoder_position()
    
    # Sequence to run:
    # Both wheels forward 4 cm/s for 5 sec
    # Left wheel forward 1 cm/s, Right wheel backward 1 cm/s for 2 sec
    # Both wheels backward at 6 cm/s for 3 sec
    
    # Run the motors to the speed passed in
    # Must set each motor effort individually
    drivetrain.set_speed(4, 4)
    time.sleep(5)
    
    drivetrain.set_speed(1, -1)
    time.sleep(2)
    
    drivetrain.set_speed(-6, -6)
    time.sleep(3)
    
    drivetrain.stop()
    
    # Blink LED to signal completion
    board.led_blink(5) # blink at 5 Hz
    time.sleep(2)
    board.led_off()
        
# Second Sequence
def motion_sequence_two():
        
    # Robot initial condition - reset encoders to zero
    drivetrain.stop()
    drivetrain.reset_encoder_position()
    
    # Sequence to run:
    # Left wheel 3 cm/s, Right wheel 5 cm/s for 6 sec
    # Left wheel 5 cm/s, Right wheel 6 cm/s for 6 sec 
        
    # Run the motors to the speed passed in
    # Must set each motor effort individually
    drivetrain.set_speed(3, 5)
    time.sleep(6)
    
    drivetrain.set_speed(5, 6)
    time.sleep(6)
    
    drivetrain.stop()
    
    # Blink LED to signal completion
    board.led_blink(5) # blink at 5 Hz
    time.sleep(2)
    board.led_off()

# PROGRAM START

# Blink LED to signal successful boot and program load
board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()

print("Ready to run")
board.wait_for_button() # wait to run code until USER button is pressed
time.sleep(1)
motion_sequence_one() # switch commented line depending which sequence to run
# motion_sequence_two()
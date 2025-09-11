# Lab 2 Part 1 - PWM Effort vs. Linear Speed
# SYSEN 5411 Fall 2025
# Author: Jonathan Lloyd
# Last update: Sept 10, 2025

# Goal:
# Plot robot linear speed for 4 values of open loop effort control

from XRPLib.defaults import * # Initializes board, motors, servo, and sensors
import time
import math

# main function definition
def open_loop_effort_run(effort):
    
    # Robot initial condition - reset encoders to zero
    drivetrain.stop()
    drivetrain.reset_encoder_position()
    
    # Run the motors to the level of effort passed in
    # Must set each motor effort individually
    drivetrain.set_effort(effort, effort)
    time.sleep(1) # allow robot to steady state velocity
    
    # Sample both wheel speeds in RPM to create average 
    speedSampleVectorLeft = []
    speedSampleVectorRight = []
    for i in range(10): # 10 samples
        speedSampleVectorLeft.append(left_motor.get_speed())
        speedSampleVectorRight.append(right_motor.get_speed())
        time.sleep(0.5) # sample every half second
        
    drivetrain.stop()
    
    # Data processing of sampled lists
    averageRPMLeft = sum(speedSampleVectorLeft) / len(speedSampleVectorLeft)
    averageRPMRight = sum(speedSampleVectorRight) / len(speedSampleVectorRight)
    
    # Convert average RPM to average linear speed via second function
    averageLinearLeft = motor_rpm_to_wheel_speed_conversion(averageRPMLeft)
    averageLinearRight = motor_rpm_to_wheel_speed_conversion(averageRPMRight)
    
    # Blink LED to signal completion
    board.led_blink(5) # blink at 5 Hz
    time.sleep(2)
    board.led_off()
    
    return [effort, averageLinearLeft, averageLinearRight]
    
# Conversion Function 
def motor_rpm_to_wheel_speed_conversion(motorRPM):
    
    # convert motor RPM to wheel RPM
    xrpGearReduction = 1/48 # ratio of wheel gear to motor gear
    wheelRPM = motorRPM * xrpGearReduction 
    
    # convert wheel RP to linear speed in cm/sec
    xrpWheelRadius = 6 # centimeters
    linearSpeed = wheelRPM * 2 * math.pi * xrpWheelRadius * 60 # cm/s
    
    return linearSpeed

# PROGRAM START

# run program for efforts of 0.25, 0.5, 0.75, 1.0
print("Ready to run 1")
board.wait_for_button() # wait to run code until USER button is pressed
time.sleep(1)
runResult25 = open_loop_effort_run(0.25)

print("Ready to run 2")
board.wait_for_button()
time.sleep(1)
runResult50 = open_loop_effort_run(0.50)

print("Ready to run 3")
board.wait_for_button()
time.sleep(1)
runResult75 = open_loop_effort_run(0.75)

print("Ready to run 4")
board.wait_for_button()
time.sleep(1)
runResult100 = open_loop_effort_run(1.0)

print("Effort Level, Left Motor, Right Motor")
print(runResult25)
print(runResult50)
print(runResult75)
print(runResult100)

# format data for export
resultsMatrix = []
resultsMatrix.append(runResult25)
resultsMatrix.append(runResult50)
resultsMatrix.append(runResult75)
resultsMatrix.append(runResult100)

print("Results Matrix")
print(resultsMatrix)

# DATA PROCESSING NOT POSSIBLE ON MICROPYTHON - RUN ON COMPUTER
# Copy out resultsMatrix and paste into data processing script, or export to CSV
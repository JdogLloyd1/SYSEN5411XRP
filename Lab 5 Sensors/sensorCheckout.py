# Sensor Checkout Protocol
# Paste block by block into XRP command prompt

from XRPLib.defaults import *
import time

# ---- Ultrasonic Rangefinder ----
d_cm = rangefinder.distance()
print("Ultrasonic readings (cm):")
print(d_cm)
time.sleep(3)

# ---- Line/Reflectance Sensor ----
print("Reflectance (left, right):")
for _ in range(10):
    l = reflectance.get_left()
    r = reflectance.get_right()
    print(l, r)
    time.sleep(0.2)

#---- IMU ----
print("IMU (pitch, roll, yaw, heading):")
for _ in range(10):
    p = imu.get_pitch()
    r = imu.get_roll()
    y = imu.get_yaw()
    h = imu.get_heading() # heading in degrees, 0–360 typically
    print(p, r, y, h)
    time.sleep(0.2)

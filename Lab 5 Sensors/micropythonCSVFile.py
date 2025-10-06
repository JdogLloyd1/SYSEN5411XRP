# File read/write 101
# store data onboard XRP as text/CSV then pull to laptop via Thonny

import time

with open('readings.csv', 'w') as f:
    f.write('t_ms,heading_deg,range_cm\n') # header
    t0 = time.ticks_ms()
    for i-
    in range(5):
        try:
            hdg = imu.get_heading()
            rng = rangefinder.distance()
        except:
            hdg, rng = -1, -1
        t = time.ticks_diff(time.ticks_ms(), t0)
        f.write(f"{t},{hdg},{rng}\n")
        time.sleep(0.25)

print("Wrote readings.csv")

# txt write test
from XRPLib.defaults import * # Initializes board, motors, servo, and sensors
import time
import math

board.led_blink(5) # blink at 5 Hz
time.sleep(2)
board.led_off()

stst_timer = 0.015
tst_timer = 0.5
target_vector = [0, 0, 195]

# with open("timer_log.txt", "wb") as f:
#     f.write("Target Vector: \n")
#     f.write(f"{target_vector}\n")
#     f.write("STST Timer: \n")
#     f.write(f"{stst_timer}\n")
#     f.write("TST Timer: \n")
#     f.write(f"{tst_timer}\n")

# with open('timer_log '+ str(target_vector) +'.csv', 'w') as file:
#     file.write(','.join("Target Vector: ") + '\n')
#     file.write(','.join(str(target_vector)) + '\n')
#     file.write(','.join("STST Timer: ") + '\n')
#     file.write(','.join(str(stst_timer)) + '\n')
#     file.write(','.join("TST Timer: ") + '\n')
#     file.write(','.join(str(tst_timer)) + '\n')


# Set board light to green to signify code complete
board.set_rgb_led(0,255,0) # range 0-255 for each r,g,b

import numpy as np
import math
import screen_brightness_control as sbc

def handle_brightness_control(lmlist):
    x1, y1 = lmlist[4][1:]
    x2, y2 = lmlist[20][1:]
    length = math.hypot(x2 - x1, y2 - y1)
    b_level = np.interp(length, [15, 220], [0, 100])
    sbc.set_brightness(int(b_level))
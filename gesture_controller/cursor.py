import autopy
import numpy as np
from utils.config import screen_width, screen_height, smoothening

prev_x, prev_y = 0, 0

def handle_cursor_control(lmlist):
    global prev_x, prev_y
    x1, y1 = lmlist[8][1:]
    x3 = np.interp(x1, (100, screen_width - 100), (0, screen_width))
    y3 = np.interp(y1, (100, screen_height - 100), (0, screen_height))
    curr_x = prev_x + (x3 - prev_x) / smoothening
    curr_y = prev_y + (y3 - prev_y) / smoothening
    autopy.mouse.move(screen_width - curr_x, curr_y)
    prev_x, prev_y = curr_x, curr_y
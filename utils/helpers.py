def detect_gesture_mode(fingers):
    if fingers == [0, 1, 0, 0, 0]:
        return "cursor"
    elif fingers == [1, 1, 0, 0, 0]:
        return "volume"
    elif fingers == [1, 0, 0, 0, 1]:
        return "brightness"
    return "system"
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
minVol, maxVol = volume.GetVolumeRange()[:2]

def handle_volume_control(lmlist):
    x1, y1 = lmlist[4][1:]
    x2, y2 = lmlist[8][1:]
    length = math.hypot(x2 - x1, y2 - y1)
    vol = np.interp(length, [15, 220], [minVol, maxVol])
    volume.SetMasterVolumeLevel(vol, None)
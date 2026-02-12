import os
import sounddevice as sd
import numpy as np
import time

clap_times = []

# Settings
THRESHOLD = 35          # adjust based on your mic sensitivity
DOUBLE_CLAP_DELAY = 1.0 # max seconds allowed between claps
COMMAND = "start chrome https://www.youtube.com"  # change to any app/site

def detect_clap(indata, frames, time_info, status):
    global clap_times
    volume_norm = np.linalg.norm(indata) * 10
    print(volume_norm)  # live volume levels for tuning

    if volume_norm > THRESHOLD:
        now = time.time()
        clap_times.append(now)

        # Keep only the last 2 claps
        if len(clap_times) > 2:
            clap_times = clap_times[-2:]

        # Check for double clap
        if len(clap_times) == 2 and clap_times[-1] - clap_times[-2] < DOUBLE_CLAP_DELAY:
            print("👏 Double clap detected! Opening...")
            os.system(COMMAND)
            clap_times.clear()  # reset after action

with sd.InputStream(callback=detect_clap):
    print("Listening for double claps... Press Ctrl+C to stop.")
    while True:

        time.sleep(0.1)

# Description: New and improved threaded client for Burton on the RPI
# Author: Brandon Palomino
# Date: 12/10/17
# Version: 6.0

import snowboythreaded
import sys
import signal
import time
from burton import Burton
import functools

print = functools.partial(print, flush=True)
pause = False
stop_program = False
burton = Burton()

def startBurton():
    global pause
    pause = True

def signal_handler(signal, frame):
    global stop_program
    stop_program = True

models = ['resources/Burton.pmdl']
sensitivity=[0.4]
callbacks = [startBurton]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

# Initialize ThreadedDetector object and start the detection thread
threaded_detector = snowboythreaded.ThreadedDetector(models, sensitivity=sensitivity)
threaded_detector.start()

print('Listening... Press Ctrl+C to exit')

# main loop
threaded_detector.start_recog(sleep_time=0.03, detected_callback=callbacks)

# Let audio initialization happen before requesting input
time.sleep(1)

burton.pixels.off() #making sure lights off before starting again
while not stop_program:
    if pause:
        try:
            threaded_detector.freeAudioResources()
            burton.runOnce()
            threaded_detector.restart()
        except OSError as e:
            print("OSError with pyaudio, restarting...")
            print(e.args)
            break
        pause = False

threaded_detector.terminate()

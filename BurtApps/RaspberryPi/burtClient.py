# Description: burton client
# Author: Brandon Palomino
# Date: 11/30/17
# Version: 6.0

import snowboydecoder
import sys
import signal
from burton import Burton

interrupted = False
burton = Burton()

model = "resources/Burton.pmdl"
detector = None

def startBurton():
	global detector
	# snowboydecoder.play_audio_file()
	detector.terminate()
	burton.runOnce()

	detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
	detector.start(detected_callback=startBurton,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

	
def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=startBurton,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

# detector.terminate()

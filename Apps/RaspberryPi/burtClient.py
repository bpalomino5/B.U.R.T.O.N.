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

models = ['resources/Burton.pmdl','resources/toggle.listener.pmdl']
detector = None
sensitivity=[0.4,0.5]

def startBurton():
  global detector
  detector.terminate()
  burton.runOnce()
  detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
  detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

def toggleListener():
  burton.play("sounds/stop.mp3")
  burton.listening = not burton.listening

callbacks = [startBurton, toggleListener]


def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted


# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=callbacks,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

# detector.terminate()

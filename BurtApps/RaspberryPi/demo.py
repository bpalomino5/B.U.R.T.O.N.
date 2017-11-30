import snowboydecoder
import sys
import signal

interrupted = False

def startBurton():
	snowboydecoder.play_audio_file()

def signal_handler(signal, frame):
    global interrupted
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

model = "resources/Burton.pmdl"

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
print('Listening... Press Ctrl+C to exit')

# main loop
detector.start(detected_callback=startBurton,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()

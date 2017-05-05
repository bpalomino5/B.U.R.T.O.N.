import time
import speech_recognition as sr

StartCommand = 'Jarvis'
callbackStr = None

print 'In backgroundListen.py'

# this is called from the background thread
def callback(recognizer, audio):
    global callbackStr
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
        callbackStr = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


rec = sr.Recognizer()
mic = sr.Microphone()
with mic as source:
    rec.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

# start listening in the background (note that we don't have to do this inside a `with` statement)
print 'starts listening'
stop_listening = rec.listen_in_background(mic, callback, 5)
# `stop_listening` is now a function that, when called, stops background listening

# do some other computation for 5 seconds, then stop listening and keep doing other computations
# for _ in range(50): time.sleep(0.1)  # we're still listening even though the main thread is doing other things
# stop_listening()  # calling this function requests that the background listener stop listening
while True:  
    time.sleep(5)
    rec.adjust_for_ambient_noise(source)
    print 'ambient noise: ', rec.energy_threshold
    if callbackStr == StartCommand:
        print 'Stop listening'
        stop_listening()
        break
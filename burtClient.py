# Description: B.U.R.T.O.N. AI assistant using wit.ai, Uberi, and Python
# Author: Brandon Palomino
# Date: 10/16/17
# Version: 5.0

# For AWS Polly
from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from tempfile import gettempdir
import os

import requests
from subprocess import call
import speech_recognition as sr
import datetime
import time
import json
#from playsound import playsound
from Led.pixels import Pixels

# token for accessing burton server
token='mytoken'

# Voice source switch
voiceSourceMac = False

# aws polly client
session = Session(profile_name="default")
polly = session.client("polly")

# objects for Uberi Speech Recognition
r = sr.Recognizer()
m = sr.Microphone()

# setup for speech recognition object
with m as source: 
		r.energy_threshold = 4000
		r.pause_threshold = 0.5
		r.operation_timeout=2

# pixels object
pixels = Pixels()

def speechAWS(phrase):
	try:
	    # Request speech synthesis
	    response = polly.synthesize_speech(TextType="ssml", Text="<speak><prosody rate=\"+1.2\" volume=\"x-loud\">"+ phrase +".</prosody></speak>", OutputFormat="mp3", VoiceId="Brian")
	except (BotoCoreError, ClientError) as error:
	    # The service returned an error, exit gracefully
	    print(error)

	# Access the audio stream from the response
	if "AudioStream" in response:
	    with closing(response["AudioStream"]) as stream:
	        output = os.path.join(gettempdir(), "speech.mp3")
	        try:
	            # Open a file for writing the output as a binary stream
	        	with open(output, "wb") as file:
	        		file.write(stream.read())
	        	
	        	if voiceSourceMac:
	        		playsound(output)
	        	else:
					call(["mplayer","-ao", "alsa", "-really-quiet", "-noconsolecontrols", "/tmp/speech.mp3"])
	        except IOError as error:
	            # Could not write to file, exit gracefully
	            print(error)
	else:
	    print("Could not stream audio")

def spch2Txt():
	play("sounds/stop.mp3")
	pixels.listen();
	try:
			with m as source: audio = r.listen(source,2)
	except sr.WaitTimeoutError:
		return ""

	try:
		value = r.recognize_google(audio)						

		if str is bytes:  # this version of Python uses bytes for strings (Python 2)
			print '{:<11}{:<0}'.format("User:",format(value).encode("utf-8"))
        	return format(value).encode("utf-8")
	except sr.UnknownValueError:
		print '{:<11}{:<0}'.format("Assistant:","Sorry, I did not understand")
		say("Sorry, I did not understand")
		return ""
	except sr.RequestError as e:
		print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
		say("Sorry, my brain is working at the moment")
		return ""

def play(file):
	if voiceSourceMac:
		playsound(file)
	else:
		call(["mplayer","-ao", "alsa", "-really-quiet", "-noconsolecontrols", file])

def say(phrase):
	if voiceSourceMac:
		speechMAC(phrase)
	else:
		speechAWS(phrase)

def speechMAC(phrase):
	call(["say", str(phrase)])

def checkHotword(phrase):
	global checkList,callbackStr
	checkList = callbackStr.split(' ', 1)
	return checkList[0] == StartCommand or checkList[0] == 'Britain'

def callback(recognizer, audio):
    global callbackStr
    # received audio data, now we'll recognize it using Google Speech Recognition
    try:
        callbackStr = recognizer.recognize_google(audio)
    except sr.UnknownValueError:
    	# do nothing, print("Google Speech Recognition could not understand audio")
    	pass
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def send_message(token, text):
  if not text:	#will not send message if text null
  	return
  pixels.think()
  r = requests.post('https://afternoon-cove-17562.herokuapp.com/',
    params={"access_token": token},
    data=json.dumps({
      "message": {"text": text.decode('unicode_escape')}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print r.text
  else:
  	print '{:<11}{:<0}'.format("Assistant:",r.text)
  	say(r.text)

def getRequest():
	return spch2Txt()

if __name__ == '__main__':
	StartCommand = 'Burton'
	callbackStr = ""
	checkList = None
	stop_listening = r.listen_in_background(m, callback, 3)

	try:
	    while True:
	    	# leaving a time sleep for 1/10th a second for now, works faster
	      	time.sleep(0.00001)
	      	if checkHotword(callbackStr):
	            pixels.wakeup()
	            print '{:<11}{:<0}'.format("User:",callbackStr)
	            play("sounds/start.mp3")
	          
	            # Stop handler that is listening in the background
	            stop_listening()

	            # starts here
	            if len(checkList)>1 :
	            	send_message(token,checkList[1])
	            else:
	            	send_message(token, getRequest())
	            pixels.off()
	            # Print line to indicate end of session
	            print "-" * 50
	            # Start background listening again
	            stop_listening = r.listen_in_background(m, callback, 3)
	        # Reset callbackstr for next session
	        callbackStr=""
	except KeyboardInterrupt:
		print "Terminating Program"
		pixels.off()

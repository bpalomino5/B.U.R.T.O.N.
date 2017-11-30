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

class Burton(object):
	"""docstring for Burton"""
	def __init__(self, voiceSourceMac=False):
		self.token = 'mytoken'
		self.voiceSourceMac=voiceSourceMac
		self.session = Session(profile_name="default")
		self.polly = self.session.client("polly")
		self.r = sr.Recognizer()
		self.m = sr.Microphone()
		self.checkList=None
		self.callbackStr=""
		self.StartCommand = "Burton"

		#setting up objects for sr
		with self.m as source:
			self.r.energy_threshold = 4000
			self.r.pause_threshold = 0.5
			self.r.operation_timeout=2

		self.pixels = Pixels()

	def speechAWS(self, phrase):
		try:
		    # Request speech synthesis
		    response = self.polly.synthesize_speech(TextType="ssml", Text="<speak><prosody rate=\"+1.2\" volume=\"x-loud\">"+ phrase +".</prosody></speak>", OutputFormat="mp3", VoiceId="Brian")
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
		        	
		        	if self.voiceSourceMac:
		        		playsound(output)
		        	else:
						call(["mplayer","-ao", "alsa", "-really-quiet", "-noconsolecontrols", "/tmp/speech.mp3"])
		        except IOError as error:
		            # Could not write to file, exit gracefully
		            print(error)
		else:
		    print("Could not stream audio")

	def spch2Txt(self):
		self.play("sounds/stop.mp3")
		self.pixels.listen();
		try:
				with self.m as source: audio = self.r.listen(source,2)
		except sr.WaitTimeoutError:
			return ""

		try:
			value = self.r.recognize_google(audio)						

			if str is bytes:  # this version of Python uses bytes for strings (Python 2)
				print '{:<11}{:<0}'.format("User:",format(value).encode("utf-8"))
		      	return format(value).encode("utf-8")
		except sr.UnknownValueError:
			print '{:<11}{:<0}'.format("Assistant:","Sorry, I did not understand")
			self.say("Sorry, I did not understand")
			return ""
		except sr.RequestError as e:
			print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
			self.say("Sorry, my brain is working at the moment")
			return ""

	def play(self,file):
		if self.voiceSourceMac:
			playsound(file)
		else:
			call(["mplayer","-ao", "alsa", "-really-quiet", "-noconsolecontrols", file])

	def say(self,phrase):
		if self.voiceSourceMac:
			self.speechMAC(phrase)
		else:
			self.speechAWS(phrase)

	def speechMAC(self,phrase):
		call(["say", str(phrase)])

	def send_message(self,token, text):
		if not text:	#will not send message if text null
			return
		self.pixels.think()
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
			self.say(r.text)

	def getRequest(self):
		return self.spch2Txt()

	def checkHotword(self,phrase):
		self.checkList = self.callbackStr.split(' ', 1)
		return self.checkList[0] == self.StartCommand or self.checkList[0] == 'Britain'

	def callback(self,recognizer, audio):
		try:
			self.callbackStr = recognizer.recognize_google(audio)
		except sr.UnknownValueError:
			# do nothing, print("Google Speech Recognition could not understand audio")
			pass
		except sr.RequestError as e:
		    print("Could not request results from Google Speech Recognition service; {0}".format(e))

	def run(self):
		stop_listening = self.r.listen_in_background(self.m, self.callback, 3)
		try:
			while True:
				time.sleep(0.00001)
				if self.checkHotword(self.callbackStr):
					self.pixels.wakeup()
					print '{:<11}{:<0}'.format("User:",self.callbackStr)
					self.play("sounds/start.mp3")

					# Stop handler that is listening in the background
					stop_listening()

					# starts here
					if len(self.checkList)>1 :
						self.send_message(self.token,self.checkList[1])
					else:
						self.send_message(self.token, self.getRequest())
					self.pixels.off()
					# Print line to indicate end of session
					print "-" * 50
					# Start background listening again
					stop_listening = self.r.listen_in_background(self.m, self.callback, 3)
				self.callbackStr=""
		except KeyboardInterrupt:
			print "Terminating Program"
			self.pixels.off()

if __name__ == '__main__':
	# example run of object
	b = Burton()
	b.run()
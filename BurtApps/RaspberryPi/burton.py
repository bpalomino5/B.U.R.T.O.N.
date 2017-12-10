# Description: burton class file for accessing with burton client
# Author: Brandon Palomino
# Date: 11/30/17
# Version: 6.0

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
from QueryGoogle.queryHandler import runQuery

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
		self.listening = True

		#setting up objects for sr
		with self.m as source:
			self.r.energy_threshold = 4000
			self.r.pause_threshold = 0.5
			self.r.operation_timeout=3

		self.pixels = Pixels()

	def speechAWS(self, phrase):
		try:
		  # Request speech synthesis
		  response = self.polly.synthesize_speech(TextType="ssml", Text="<speak><prosody rate=\"+1.0\" volume=\"x-loud\">"+ phrase +".</prosody></speak>", OutputFormat="mp3", VoiceId="Brian")
		except (BotoCoreError, ClientError) as error:
		  # The service returned an error, exit gracefully
		  print(error)

		# Access the audio stream from the response
		if "AudioStream" in response:
			with closing(response["AudioStream"]) as stream:
				output = os.path.join(gettempdir(), "speech.mp3")
				try:
					with open(output, "wb") as file: file.write(stream.read())
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
		self.play("sounds/start.mp3")
		self.pixels.listen();
		try:
			with self.m as source: audio = self.r.listen(source,4)
		except sr.WaitTimeoutError:
			self.play("sounds/stop.mp3")
			return ""

		try:
			value = self.r.recognize_google(audio)						

			if "Google" in format(value):
				input = os.path.join(gettempdir(), "in.wav")
				with open(input,"wb") as f:
					f.write(audio.get_wav_data(16000))

			print('{:<11}{:<0}'.format("User:",format(value)))
			return format(value)
		except sr.UnknownValueError:
			print('{:<11}{:<0}'.format("Assistant:","Sorry, I did not understand"))
			# self.say("Sorry, I did not understand")
			self.play("sounds/stop.mp3")
			return ""
		except sr.RequestError as e:
			print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
			self.say("Sorry, my brain is not working at the moment")
			quit() #reset burton client
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
		if "Google" in text:
			# print("needs to use google handler")
			response = runQuery()
			if not response:
				return
			print('{:<11}{:<0}'.format("Assistant:",response))
			self.say(response)
		else:
			r = requests.post('https://afternoon-cove-17562.herokuapp.com/',
			  params={"access_token": token},
			  data=json.dumps({
			    "message": {"text": text}
			  }),
			  headers={'Content-type': 'application/json'})
			if r.status_code != requests.codes.ok:
			  print(r.text)
			else:
				if not r.text:
					return
				print('{:<11}{:<0}'.format("Assistant:",r.text))
				self.say(r.text)

	def getRequest(self):
		return self.spch2Txt()

	def runOnce(self):
		if self.listening:
			self.pixels.wakeup()
			print('{:<11}{:<0}'.format("User:",self.StartCommand))
			self.send_message(self.token, self.getRequest())
			self.pixels.off()
			print("-" * 60)

if __name__ == '__main__':
	# example run of object
	b = Burton()
	b.runOnce()

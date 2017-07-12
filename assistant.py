# Description: Version 3 of myservant.py using wit.ai, Uberi, and Python
# Author: Brandon Palomino
# Date: 4/8/17

#following sends an imessage to elaine only if messages app is open
#osascript -e 'tell application "Messages" to send "Hello World" to buddy "Elaine Heng"'
# does both
# open -a Messages && osascript -e 'tell application "Messages" to send "Hello World" to buddy "Elaine Heng"'

from boto3 import Session
from botocore.exceptions import BotoCoreError, ClientError
from contextlib import closing
from tempfile import gettempdir
import os

import sys
from random import shuffle, randint
from wit import Wit
from subprocess import call
import speech_recognition as sr
import datetime
import time
from weather import Weather
#from playsound import playsound
from flask import Flask, request
from multiprocessing import Process

# For flask server
app = Flask(__name__)

# Voice source switch
voiceSourceMac = False

# Speech Switch
global usePhoneSpeaker

# Create a client using the credentials and region defined in the [adminuser]
# section of the AWS credentials file (~/.aws/credentials).
session = Session(profile_name="default")
polly = session.client("polly")

# weather object handler
w = Weather()

# objects for Uberi Speech Recognition
r = sr.Recognizer()
m = sr.Microphone()

# token to call wit.ai API
access_token = "OF4G7O5U4MBAQU5GMSZUOUIHBMLYD4QV"

# Timestamp variable for session_id
TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

# Response holder
global bResponse

# hard coded replies to intents
all_replies = {
    'compliment': [
        'The greatest master I have ever served!',
        'A Peruvian Genius!',
    ],
    'gratitude': [
    	'The pleasure is mine sir'
    ],
    'negative' : [
    	'my apologies sir',
    	'my apologies, let me try again',
    	'unfortunately, my master did not design me perfectly',
    ],
    'positive' : [
    	'that is great to hear sir',
    	'splendid sir',
    ],
}

all_farewells = {
	'default' : 'farewell sir',
	'late' : 'good night sir',
}
all_greetings = {
	'default' : 'hello sir',
	'morning' : 'good morning sir',
	'afternoon' : 'good afternoon sir',
	'evening' : 'good evening sir',
}

all_animes = {
	'Hero Academia' : 'http://kissanime.ru/Anime/Boku-no-Hero-Academia-2nd-Season',
	'Attack on Titan' : 'http://kissanime.ru/Anime/Shingeki-no-Kyojin-2nd-Season',
	'Dragon Ball Super': 'http://kissanime.ru/Anime/Dragon-Ball-Super',
	'Fullmetal Alchemist': 'http://kissanime.ru/Anime/Fullmetal-Alchemist-Brotherhood',
}

all_users = {
	'Brandon' : 'My master',
	'Elaine' : 'Elaine is the princess',
	'Brian' : 'A humble servant to my master',
	'Unknown' : [
		'Someone I\'m not familiar with.',
		'Clearly someone not very important, or else I would have known of such a person'
	],
}

def speechAWS(phrase):
	# session = Session(profile_name="default")
	# polly = session.client("polly")

	try:
	    # Request speech synthesis
	    response = polly.synthesize_speech(TextType="ssml", Text="<speak><prosody rate=\"+1.2\" volume=\"x-loud\">"+ phrase +".</prosody></speak>", OutputFormat="mp3",
	                                        VoiceId="Brian")
	except (BotoCoreError, ClientError) as error:
	    # The service returned an error, exit gracefully
	    print(error)
	    #sys.exit(-1)

	# Access the audio stream from the response
	if "AudioStream" in response:
	    # Note: Closing the stream is important as the service throttles on the
	    # number of parallel connections. Here we are using contextlib.closing to
	    # ensure the close method of the stream object will be called automatically
	    # at the end of the with statement's scope.
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
	            #sys.exit(-1)

	else:
	    # The response didn't contain audio data, exit gracefully
	    print("Could not stream audio")
	    #sys.exit(-1)

# method to receive speech to text input
def spch2Txt():
	#print("A moment of silence, please...")
	with m as source: r.adjust_for_ambient_noise(source)
	#print("Set minimum energy threshold to {}".format(r.energy_threshold))
	# print("Say something!")
	#print 'User:     ',
	#sys.stdout.flush()
	# say("+")				#simple sound to indicate read to process speech input
	if voiceSourceMac:
		playsound("QueryBeep.m4a")
	else:
		call(["mplayer","-ao", "alsa", "-really-quiet", "-noconsolecontrols", "QueryBeep.m4a"])
	with m as source: audio = r.listen(source)
	#print("Got it! Now to recognize it...")
	try:
        # recognize speech using Google Speech Recognition
		value = r.recognize_google(audio)						#used to use google speech recognition, but changed to wit speech api
		# value = r.recognize_wit(audio, key=access_token)

        # we need some special handling here to correctly print unicode characters to standard output
		if str is bytes:  # this version of Python uses bytes for strings (Python 2)
			#print(format(value).encode("utf-8"))
			print '{:<11}{:<0}'.format("User:",format(value).encode("utf-8"))
        	return format(value).encode("utf-8")
	except sr.UnknownValueError:
		#print("Sorry, I did not understand")
		print '{:<11}{:<0}'.format("Assistant:","Sorry, I did not understand")

		if voiceSourceMac:
			say("Sorry, I did not understand")
		else:
			speechAWS("Sorry, I did not understand")
		
		return spch2Txt()
	except sr.RequestError as e:
		print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
		return ""

def say(phrase):
	call(["say", str(phrase)])

def first_entity_value(entities, entity):
    if entity not in entities:
        return None
    val = entities[entity][0]['value']
    if not val:
        return None
    return val['value'] if isinstance(val, dict) else val

def send(request, response):
	global bResponse
	print '{:<11}{:<0}'.format("Assistant:",response['text'])
    
    # store response
	bResponse = response['text']
	
	global usePhoneSpeaker
	if usePhoneSpeaker == False:
		if voiceSourceMac:
			say(response['text'])
		else:
			speechAWS(response['text'])

def getGreeting():
	if randint(0,1) == 1:
		return 'default'
	hour = int(datetime.datetime.now().strftime("%H"))
	if hour >=6 and hour < 12:
		return 'morning'
	elif hour >= 12 and hour < 17:
		return 'afternoon'
	elif hour >= 17 or hour < 1:
		return 'evening'
	else:
		return 'default'


def replyGreeting(request):
    context = request['context']
    entities = request['entities']

    greeting = first_entity_value(entities, 'greeting')

    if greeting:
        response = all_greetings[getGreeting()]
        context['greeting'] = response
    else:
		context['greeting'] = all_greetings['default']
    return context

def reply_Gratitude(request):
	context = request['context']
	replies = all_replies['gratitude']
	context['gratitude'] = replies[0]
	return context

def returnComp(request):
    context = request['context']
    replies = all_replies['compliment']
    shuffle(replies)
    context['compliment'] = replies[0]
    return context

def getFarewell():
	hour = int(datetime.datetime.now().strftime("%H"))
	if hour >= 22 or hour < 5:
		return 'late'
	else:
		return 'default'
def replyFarewell(request):
    context = request['context']
    farewell = all_farewells[getFarewell()]
    context['farewell'] = farewell
    return context

def openMyAnime(request):
    context = request['context']
    entities = request['entities']

    anime = first_entity_value(entities, 'anime')
    
    if anime:
    	animeLink = all_animes[anime]
       	call(["open", animeLink])

        if context.get('missingAnime') is not None:
        	del context['missingAnime']
    else:
        context['missingAnime'] = True
        if context.get('anime') is not None:
            del context['anime']

    return context

def get_User(request):
	context = request['context']
	entities = request['entities']

	user = first_entity_value(entities, 'User')

	if user:
		userDescription = all_users[user]
		context['User'] = userDescription
	else:
		unknownUserReplies = all_users['Unknown']
		shuffle(unknownUserReplies)
		context['User'] = unknownUserReplies[0]

	return context

def get_forecast(request):
	context = request['context']
	entities = request['entities']

	loc = first_entity_value(entities, 'location')
	#loc = 'Pomona'
	if loc:
		if loc == 'here':
			loc = 'Pomona'
		w.getWeather(loc)
		context['forecast'] = w.getDescription()
		if context.get('missingLocation') is not None:
			del context['missingLocation']
	else:
		context['missingLocation'] = True
		if context.get('forecast') is not None:
			del context['forecast']
	return context

def flip_lightSwitch(request):
	context = request['context']
	entities = request['entities']

	setting = first_entity_value(entities, 'toggle')
    
	if setting:
		if setting == "on":
			call(["ssh", "pi@192.168.0.17", "python Code/switchLights.py 0"])
		elif setting == "off":
			call(["ssh", "pi@192.168.0.17", "python Code/switchLights.py 1"])
		context['setting'] = setting
	return context

def reply_Sentiment(request):
	context = request['context']
	entities = request['entities']

	sentiment = first_entity_value(entities, 'sentiment')

	if sentiment:
		responses = all_replies[sentiment]
		shuffle(responses)
		context['sentimentResponse'] = responses[0]
	return context			

def tell_Time(request):
	context = request['context']
	time = datetime.datetime.now().strftime("%I:%M %p")
	context['time'] = time
	return context

def recite_Phrase(request):
    context = request['context']
    entities = request['entities']

    phrase = first_entity_value(entities, 'message_body')
    context['phrase'] = phrase
    return context

actions = {
    'send': send,
    'replytoGreeting': replyGreeting,
    'replytoFarewell': replyFarewell,
    'returnCompliment': returnComp,
    'openAnime' : openMyAnime,
    'getUser' : get_User,
    'getForecast' : get_forecast,
    'replyGratitude' : reply_Gratitude,
    'fliplightSwitch' : flip_lightSwitch,
    'replySentiment' : reply_Sentiment,
    'tellTime': tell_Time,
    'recitePhrase' : recite_Phrase,
}
 

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

with m as source: r.adjust_for_ambient_noise(source)
stop_listening = r.listen_in_background(m, callback, 5)

# init wit client object with token
client = Wit(access_token=access_token, actions=actions)
# session_id = 'user-session-'+ TIMESTAMP

usePhoneSpeaker = False

def getSessionID():
	TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
	return 'user-session-' + TIMESTAMP

def analyzeRequest(resp, command=None):
	# Create new session id for each interaction session with wit.ai
	session_id = getSessionID()

	if command:
		resp = client.run_actions(session_id, command, resp)
	else:
		resp = client.run_actions(session_id, spch2Txt(),resp)

	if(resp.has_key('missingAnime') or resp.has_key('missingLocation')):
		analyzeRequest(resp)
	if(resp.has_key("farewell")):
		exit(0)

@app.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    resp = {}
    # check if client wants to speak through its on speaker
    global usePhoneSpeaker
    usePhoneSpeaker = request.json['toggle']
    analyzeRequest(resp, request.json['description'])
    return bResponse

def flaskProcess():
    app.run(host='192.168.0.14', port=5000)

p = Process(target=flaskProcess)
p.start()

StartCommand = 'Burton'
callbackStr = ""

try:
    while True:
    	# leaving a time sleep for 1/10th a second for now, works faster
        time.sleep(0.01)
        
        checkList = callbackStr.split(' ', 1)
        if checkList[0] == StartCommand or checkList[0] == 'Britain':
            print '{:<11}{:<0}'.format("User:",callbackStr)
            # print 'Stop listening'
            # Give indication that start command was recognized
            if voiceSourceMac:
                playsound("EntryBeep.m4a")
            else:
            	call(["mplayer","-ao", "alsa", "-really-quiet", "-noconsolecontrols", "EntryBeep.m4a"])

            # Stop handler that is listening in the background
            stop_listening()

            # Create context object to start user session
            resp = {}
            if len(checkList)>1 :
            	analyzeRequest(resp, checkList[1])
            else:
            	analyzeRequest(resp)
            # Print line to indicate end of session
            print "-" * 50
            # Start background listening again
            stop_listening = r.listen_in_background(m, callback, 5)
        # Reset callbackstr for next session
        callbackStr=""
except KeyboardInterrupt:
    print "Killing Processes"
    p.terminate()

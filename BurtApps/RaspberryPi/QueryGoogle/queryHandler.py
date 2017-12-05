from . import queryGoogle
import speech_recognition as sr
from os import path

def runQuery():
	# obtain path to "english.wav" in the same folder as this script
	AUDIO_FILE = "QueryGoogle/resources/out.wav"
	r = sr.Recognizer()

	# query google assistant api
	queryGoogle.query()

	# translate reponse from google to text
	with sr.AudioFile(AUDIO_FILE) as source:
	    audio = r.record(source)  # read the entire audio file

	# recognize speech using Google Speech Recognition
	try:
			value = r.recognize_google(audio)
			# print(r.recognize_google(audio))
			return value
	except sr.UnknownValueError:
			return ""
	    # print("Google Speech Recognition could not understand audio")
	except sr.RequestError as e:
			return ""
	    # print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == '__main__':
	runQuery()
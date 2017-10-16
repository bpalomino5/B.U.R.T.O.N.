from flask import Flask, request
import json
import requests

app = Flask(__name__)

@app.route('/index/')
def index():
    return "Hi I'm a chatbot"

##OLD CODE

# @app.route('/todo/api/v1.0/tasks', methods=['POST'])
# def create_task():
#     resp = {}
#     # check if client wants to speak through its on speaker
#     global usePhoneSpeaker
#     usePhoneSpeaker = request.json['toggle']
#     analyzeRequest(resp, request.json['description'])
#     return bResponse


#####

# @app.route('/', methods=['GET'])
# def handle_verification():
# 	print "Handling Verification."
# 	if request.args.get('hub.verify_token', '') == 'mytoken':
# 		print "Verification successful!"
# 		return request.args.get('hub.challenge', '')
# 	else:
# 		print "Verification failed!"
#     	return 'Error, wrong validation token'

@app.route('/', methods=['POST'])
def handle_messages():
	print "Handling Messages"
	if request.args.get('access_token', '') != 'mytoken':
		return 'Error, wrong validation token'
  	payload = request.get_data()
  	print payload
  	messaging_events(payload)
  	# for sender, message in messaging_events(payload):
  	#   print "Incoming from %s: %s" % (sender, message)
  	return "ok"

def messaging_events(payload):
  	"""Generate tuples of (sender_id, message_text) from the
  	provided payload.
  	"""
	data = json.loads(payload)
	messaging_events = data["message"]
	if "text" in messaging_events:
		print messaging_events["text"]

if __name__ == '__main__':
  app.run()
from flask import Flask, request
import json
import requests
from utils import wit_response

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
def replyGreeting():
  return "Hi!"

def replyFarewell():
  return "Goodbye!"



def switchON():
  r = requests.post('https://api.particle.io/v1/devices/4d002b000b51353432383931/switch?access_token=73818545064232e532e0823be7c5cfbb1a4eac75', data = {'switch':'on'})

def switchOFF():
  r = requests.post('https://api.particle.io/v1/devices/4d002b000b51353432383931/switch?access_token=73818545064232e532e0823be7c5cfbb1a4eac75', data = {'switch':'off'})

def lightSwitch(toggleValue):
  # if toggleValue == "on":
  #   switchON()
  # elif toggleValue == "off":
  #   switchOFF()
  return "Turning " + toggleValue

def nlpProcess(message):
  entities, values = wit_response(message)
  response = "Sorry, I could not understand!"
  if "greetings" in entities and "true" in values:
    response = replyGreeting()
  if "bye" in entities and "true" in values:
    response = replyFarewell()
  if "toggle" in entities and "intent" in entities and "toggle" in values:
    toggleValue = values[entities.index('toggle')]
    response = lightSwitch(toggleValue)
  return response

@app.route('/', methods=['POST'])
def handle_messages():
  print "Handling Messages"
  if request.args.get('access_token', '') != 'mytoken':
		return 'Error, wrong validation token'
  payload = request.get_data()
  # print payload
  for message in messaging_events(payload):
    print message
    response = nlpProcess(message)
    print response
  return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["message"]
  if "text" in messaging_events:
    yield messaging_events["text"]

if __name__ == '__main__':
  app.run()
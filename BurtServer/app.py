from flask import Flask, request
import json
import requests
import datetime
from utils import wit_response

app = Flask(__name__)

@app.route('/index/')
def index():
  return "Hi I'm a chatbot"

def replyGreeting():
  return "Hi!"

def replyFarewell():
  return "Good bye!"

def switchON():
  r = requests.post('https://api.particle.io/v1/devices/4d002b000b51353432383931/switch?access_token=73818545064232e532e0823be7c5cfbb1a4eac75', data = {'switch':'on'})

def switchOFF():
  r = requests.post('https://api.particle.io/v1/devices/4d002b000b51353432383931/switch?access_token=73818545064232e532e0823be7c5cfbb1a4eac75', data = {'switch':'off'})

def lightSwitch(toggleValue):
  if toggleValue == "on":
    switchON()
  elif toggleValue == "off":
    switchOFF()
  return "Turning " + toggleValue

def infoUser(User):
  if User == "Burton":
    return "Greetings. I go by the name of Burton and I am delighted to serve as an assistant. If there is anything of that you need, just ask."
  else:
    return User

def replyThanks():
  return "You're welcome!"

def getTime():
  r = requests.get('https://www.google.com/search?q=what+time+is+it')
  p1 = r.text.split('<div class="_rkc _Peb">')[1]
  time = p1.split('</div>')[0]
  return time

def nlpProcess(message):
  entities, values = wit_response(message)
  response = "Sorry, I could not understand!"
  if "command" in entities and "cancel" in values:
    return ""
  if "greetings" in entities and "true" in values:
    response = replyGreeting()
  if "bye" in entities and "true" in values:
    response = replyFarewell()
  if "toggle" in entities and "intent" in entities and "toggle" in values:
    toggleValue = values[entities.index('toggle')]
    response = lightSwitch(toggleValue)
  if "intent" in entities and "User" in entities and "whoisUser" in values:
    response = infoUser(values[entities.index('User')])
  if "thanks" in entities and "true" in values:
    response = replyThanks()
  if "intent" in entities and "time" in values:
    response = getTime()
  return response

@app.route('/', methods=['POST'])
def handle_messages():
  print "Handling Messages"
  if request.args.get('access_token', '') != 'mytoken':
		return 'Error, wrong validation token'
  payload = request.get_data()
  # print payload
  response = "Sorry, I could not understand!"
  for message in messaging_events(payload):
    print message
    response = nlpProcess(message)
    print response
  return response

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
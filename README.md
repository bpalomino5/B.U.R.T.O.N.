# B.U.R.T.O.N.
Brilliantly Useful Receptive assistant and Original Companion

## Description
My personal AI assistant which is designed using the following:

# BurtServer
- Wit.ai
- Python
- Heroku

# BurtClient
- Uberi/SpeechRecognition
- Raspberri Pi subsystems
- Python
- boto3 client services
- Amazon Web Services (AWS) - Amazon Polly
- MacOS Speech Synthesizer
- Weather.com services

## Instructions

# BurtClient
Run with: forever start -l forever.log --spinSleepTime=20000 -c python assistant.py 
Find and kill flask server with: ps -fA | grep python
Then: kill PID

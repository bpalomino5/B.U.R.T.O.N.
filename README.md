# B.U.R.T.O.N.
Brilliantly Useful Receptive assisTant and Overly-intelligent Companion

## Description
My personal A.I. assistant which is designed using the following:

- Wit.ai
- Uberi/SpeechRecognition
- Raspberri Pi subsystems
- Python
- boto3 client services
- Amazon Web Services (AWS) - Amazon Polly
- MacOS Speech Synthesizer
- Weather.com services


## Instructions
Run with: forever start -l forever.log --spinSleepTime=20000 -c python assistant.py 
Find and kill flask server with:
ps -fA | grep python
kill PID

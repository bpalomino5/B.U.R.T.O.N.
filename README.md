# B.U.R.T.O.N.
Brilliantly Useful Receptive assistant and Original Companion

# Description
My AI personal assistant which is designed using the following:

## BurtServer
- Wit.ai
- Python/Flask
- Heroku

## BurtClient
- Uberi/SpeechRecognition
- Raspberri Pi subsystems
- Python
- boto3 client services
- Amazon Web Services (AWS) - Amazon Polly
- MacOS Speech Synthesizer
- Weather.com services

## BurtApps
- JS/React Native
- Android
- IOS
- react-native-voice module
- react-native-tts module

# Instructions

## BurtClient
1) Run with: forever start -l forever.log --spinSleepTime=20000 -c python burtClient.py 
2) Find and kill flask server with: ps -fA | grep python
3) kill PID

## BurtApps
Navigate to BurtCli root directory
- For android: react-native run-android
- For IOS: react-native run-ios --device "Device Name" or run with Xcode

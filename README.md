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
![androidcli](https://user-images.githubusercontent.com/12876643/32029177-ae3de55c-b9a7-11e7-95c5-33f998b2d42e.jpg)
![ioscli](https://user-images.githubusercontent.com/12876643/32029194-c927957a-b9a7-11e7-96a8-8ec647f74751.jpg)
- JS/React Native
- Android
- IOS
- react-native-voice module
- react-native-tts module

# Instructions

## BurtClient
1) Run with: forever start -l forever.log --minUptime=1000 --spinSleepTime=20000 -c python burtClient.py 
2) Find and kill flask server with: ps -fA | grep python
3) kill PID

## BurtApps
Navigate to BurtCli root directory
- For android: react-native run-android
- For IOS: react-native run-ios --device "Device Name" or run with Xcode

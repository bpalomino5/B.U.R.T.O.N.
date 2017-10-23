import React, { Component } from 'react';
import { AppRegistry, ScrollView, StatusBar, Platform, ActivityIndicator, TextInput, Text, View , Button, StyleSheet } from 'react-native';
import Tts from 'react-native-tts';
import Voice from 'react-native-voice';

const token = "mytoken";
const url = "https://afternoon-cove-17562.herokuapp.com/?access_token=";

export default class BurtClient extends Component {
  constructor(props) {
    super(props);
    this.state = {
      text: '',
      input: '',
      response: '',

      //vars for voice
      recognized: '',
      pitch: '',
      end: '',
      started: '',
      results: [],
    };
    Voice.onSpeechStart = this.onSpeechStart.bind(this);
    Voice.onSpeechRecognized = this.onSpeechRecognized.bind(this);
    Voice.onSpeechEnd = this.onSpeechEnd.bind(this);
    Voice.onSpeechResults = this.onSpeechResults.bind(this);
    Voice.onSpeechVolumeChanged = this.onSpeechVolumeChanged.bind(this);
    Tts.setDefaultLanguage('en-GB');
    Tts.addEventListener('tts-start', (event) => console.log("start", event));
    Tts.addEventListener('tts-finish', (event) => console.log("finish", event));
    Tts.addEventListener('tts-cancel', (event) => console.log("cancel", event));
  }

  componentWillUnmount() {
    Voice.destroy().then(Voice.removeAllListeners);
  }

  onSpeechStart(e) {
    this.setState({
      started: '√',
    });
  }

  onSpeechRecognized(e) {
    this.setState({
      recognized: '√',
    });
  }

  onSpeechEnd(e) {
    if (Platform.OS === 'ios'){
      console.log(this.state.results);
      this.sendMessage(this.state.results[0]);
    }
    this.setState({
      end: '√',
    });
  }

  onSpeechResults(e) {
    if (Platform.OS === 'android'){
      this.sendMessage(e.value[0]);
    }
    this.setState({
      input: e.value[0],
      results: e.value,
    });
    this._stopRecognizing();
  }

  onSpeechVolumeChanged(e) {
    this.setState({
      pitch: e.value,
    });
  }

  async _startRecognizing(e) {
    this.setState({
      recognized: '',
      pitch: '',
      started: '',
      results: [],
      end: ''
    });
    try {
      await Voice.start('en-US');
    } catch (e) {
      console.error(e);
    }
  }

  async _stopRecognizing(e) {
    try {
      await Voice.stop();
    } catch (e) {
      console.error(e);
    }
  }

  async _cancelRecognizing(e) {
    try {
      await Voice.cancel();
    } catch (e) {
      console.error(e);
    }
  }

  async _destroyRecognizer(e) {
    try {
      await Voice.destroy();
    } catch (e) {
      console.error(e);
    }
    this.setState({
      recognized: '',
      pitch: '',
      started: '',
      results: [],
      end: ''
    });
  }

  sendMessage(message) {
    fetch(url+token, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        message: {text: message}
      })
    })
    .then(response => 
      response.text().then(data => {
        console.log(data)
        Tts.speak(data);
        this.setState({response: data});
      })
    );
  }

  render() {
    return (
      <View style={styles.container}>
        <StatusBar backgroundColor="#3E5C76" translucent/>
        <TextInput
          style={styles.inputContainer}
          underlineColorAndroid='transparent'
          placeholder={"Type Message!"}
          placeholderTextColor={"#DBDBDB"}
          onChangeText={(text) => this.setState({input:text})}
          value={this.state.input}
          onSubmitEditing={(event) => {
            console.log(event.nativeEvent.text)
            if (event.nativeEvent.text !=""){
              this.sendMessage(event.nativeEvent.text)
            }
          }}
        />
        <Text style={styles.burtonTextContainer}>Burton:</Text>
        <ScrollView style={styles.scrollContainer}>
          <Text style={{fontSize: 36}}>{this.state.response}</Text>
        </ScrollView>
        <View style={styles.buttonsViewContainer}>
          <View style={styles.buttonContainer}>
            <Button
              onPress={this._startRecognizing.bind(this)}
              title="Speak"
              color='#3E5C76'
            />
          </View>
          <View style={styles.buttonContainer}>
            <Button
              onPress={this._cancelRecognizing.bind(this)}
              title="Cancel"
              color='#3E5C76'              
            />
          </View>
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 20,
    backgroundColor: '#3E5C76' 
  },
  buttonContainer: {
    margin: 20,
    marginBottom: 20,
    width: 150
  },
  scrollContainer: {
    backgroundColor: '#E8E8E8',
    paddingLeft: 10
  },
  inputContainer: {
    height: 70,
    fontSize: 30, 
    paddingLeft: 5, 
    paddingRight: 10,
    marginTop: 5,
    marginLeft: 10,
    marginRight: 10,
    marginBottom: 10,
    color: '#E8E8E8'
  },
  burtonTextContainer: {
    paddingTop:5, 
    fontSize: 42, 
    backgroundColor: '#E8E8E8', 
    paddingLeft: 10
  },
  buttonsViewContainer: {
    backgroundColor: '#E8E8E8', 
    alignItems: 'center', 
    flexDirection: 'row', 
    justifyContent: 'center'
  }
})
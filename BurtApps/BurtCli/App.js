import React, { Component } from 'react';
import { AppRegistry, Platform, ActivityIndicator, TextInput, Text, View , Button, StyleSheet } from 'react-native';
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
        this.setState({response: data}, function() {});
      })
    );
  }

  render() {
    return (
      <View style={{paddingLeft: 20, paddingRight: 20, paddingTop: 50}}>
        <TextInput
          style={{height: 60, fontSize: 30}}
          placeholder={"Type Message!"}
          onChangeText={(text) => this.setState({input:text})}
          value={this.state.input}
          onSubmitEditing={(event) => {
            console.log(event.nativeEvent.text)
            this.sendMessage(event.nativeEvent.text)
          }}
        />
        <Text style={{paddingTop:15, fontSize: 42}}>Burton:</Text>
        <Text style={{fontSize: 36, paddingBottom: 50}}>{this.state.response}</Text>
        <View style={styles.buttonContainer}>
          <Button
            onPress={this._startRecognizing.bind(this)}
            title="Speak"
          />
        </View>
        <View style={styles.buttonContainer}>
          <Button
            onPress={this._cancelRecognizing.bind(this)}
            title="Cancel"
          />
        </View>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  buttonContainer: {
    margin: 20
  }
})
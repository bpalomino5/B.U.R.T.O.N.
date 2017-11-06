import React, { Component } from 'react';
import { 
  AppRegistry, 
  ScrollView, 
  StatusBar, 
  Platform, 
  ActivityIndicator, 
  TextInput, 
  Text, 
  View ,
  Button, 
  StyleSheet,
  TouchableOpacity,
  LayoutAnimation,
  Image
} from 'react-native';
import Tts from 'react-native-tts';
import Voice from 'react-native-voice';
import * as Progress from 'react-native-progress';

const token = "mytoken";
const url = "https://afternoon-cove-17562.herokuapp.com/?access_token=";

export default class BurtClient extends Component {
  constructor(props) {
    super(props);
    this.state = {
      //vars for requests
      text: '',
      input: '',
      response: '',

      //vars for voice
      recognized: '',
      pitch: '',
      end: '',
      started: '',
      results: [],

      //vars for mic indicator
      micOn: false,
      buttonText: 'Speak',
    };
    //bindings for voice lib
    Voice.onSpeechStart = this.onSpeechStart.bind(this);
    Voice.onSpeechRecognized = this.onSpeechRecognized.bind(this);
    Voice.onSpeechEnd = this.onSpeechEnd.bind(this);
    Voice.onSpeechResults = this.onSpeechResults.bind(this);
    Voice.onSpeechVolumeChanged = this.onSpeechVolumeChanged.bind(this);

    //events and setup for tts lib
    Tts.setDefaultLanguage('en-GB');
    Tts.addEventListener('tts-start', (event) => console.log("start", event));
    Tts.addEventListener('tts-finish', (event) => console.log("finish", event));
    Tts.addEventListener('tts-cancel', (event) => console.log("cancel", event));

    //bindings for voice lib
    this._startRecognizing = this._startRecognizing.bind(this);
    this._cancelRecognizing = this._cancelRecognizing.bind(this);
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
      micOn: false,
      buttonText: 'Speak',
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
    this.setState({
      started: ''
    });
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
          onFocus={(event) => {
            this.setState({input: ''})
          }}
        />
        <Text style={styles.burtonTextContainer}>Burton:</Text>
        <ScrollView style={styles.scrollContainer}>
          <Text style={{fontSize: 36, color: 'black'}}>{this.state.response}</Text>
        </ScrollView>
        {this.state.micOn && <Progress.CircleSnail style={styles.CircleSnail} color={'#3E5C76'} size={150} indeterminate={true} thickness={5}/>}
        <View style={styles.buttonsViewContainer}>
          <TouchableOpacity
            onPress={() => {
              if (this.state.started==''){ //listen state
                this._startRecognizing()
                LayoutAnimation.spring()
                this.setState({micOn: true})
              }
              else{ //cancel listen state
                this._cancelRecognizing()
                this.setState({micOn: false})
              }
            }}>
            <View style={styles.imageContainer}>
              <Image
                source={require('./mic.png')}
              />
            </View>
          </TouchableOpacity>
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
  imageContainer: {
    width: 100,
    height: 100,
    margin: 20,
    marginBottom: 30
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
    color: 'black',
    backgroundColor: '#E8E8E8', 
    paddingLeft: 10
  },
  buttonsViewContainer: {
    backgroundColor: '#E8E8E8', 
    alignItems: 'center', 
    flexDirection: 'row', 
    justifyContent: 'center'
  },
  CircleSnail: {
    position: 'absolute',
    top: 350,
    left: 120,
  }
})

// <View style={styles.buttonContainer}>
//             <Button
//               onPress={() => {
//                 if (this.state.started==''){ //listen state
//                   this._startRecognizing()
//                   this.state.buttonText="Cancel"
//                   LayoutAnimation.spring()
//                   this.setState({micOn: true})
//                 }
//                 else{ //cancel listen state
//                   this._cancelRecognizing()
//                   this.state.buttonText="Speak"
//                   this.setState({micOn: false})
//                 }
//               }}
//               title={this.state.buttonText}
//               color='#3E5C76'
//             />
//           </View>

// <View style={styles.buttonContainer}>
//   <Button
//     onPress={() => {
//       this._cancelRecognizing()
//       this.setState({micOn: false})
//     }}
//     title="Cancel"
//     color='#3E5C76'              
//   />
// </View>
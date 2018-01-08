import React, { Component } from 'react';
import {StyleSheet,  Text, View, Switch } from 'react-native';

const token = "mytoken";
const url = "https://afternoon-cove-17562.herokuapp.com/?access_token=";
const debugURL = "http://127.0.0.1:5000/?access_token=";

class SettingsScreen extends Component {
	constructor(props) {
		super(props);
		this.state = {
			micMuted: false
		};
		this.updateServer = this.updateServer.bind(this);
	}


	sendValue(value) {
    fetch(url+token, {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        settings: {micMuted: value}
      })
    })
    .then(response => response.json())
    .then(responseJson => {
    	// console.log(responseJson)
    });
  }

  updateServer() {
  	this.setState({micMuted: !this.state.micMuted});
  	this.sendValue(!this.state.micMuted);
  }

	render() {
		return(
			<View style={styles.container}>
				<View style={styles.itemsbox}>
					<View style={styles.rowItem}>
						<Text style={styles.itemDescription}>Mic Toggle</Text>
						<Switch
							value={this.state.micMuted}
							onValueChange={this.updateServer}
						/>
					</View>
				</View>
			</View>
		);
	}
}

const styles = StyleSheet.create({
	container: {
		padding: 16,
		flex: 1
	},
	itemsbox: {
		flex:1,
		flexDirection: 'column',
	},
	rowItem: {
		flex: 0,
		flexDirection: 'row',
		justifyContent: 'space-between'
	},
	itemDescription: {
		fontSize: 28
	},
});

export default SettingsScreen;
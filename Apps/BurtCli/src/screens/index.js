import { Navigation } from 'react-native-navigation';

import MainScreen from './MainScreen';
import SettingsScreen from './SettingsScreen';

export function registerScreens() {
	Navigation.registerComponent('bp.MainScreen', () => MainScreen);
	Navigation.registerComponent('bp.SettingsScreen', () => SettingsScreen);
}
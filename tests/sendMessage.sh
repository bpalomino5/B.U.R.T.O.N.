#!/bin/bash

open -a Messages
osascript -e 'tell application "Messages" to send "HI" to buddy "Elaine Heng"'
killall Messages
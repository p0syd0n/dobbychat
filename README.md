# dobbychat
Minimalistsic chat app written in python

The chat server repo is located here:
https://github.com/p0syd0n/chatserver

Dobbychat supports custom nicknames, private rooms. You can create rooms also.

To create a room:
click "File" menu at top of window

for a public room, enter a room name. For a private room, enter ```PRIVATE.[room-name]``` where ```[room-name]``` is your choice of name.

The config file:
You may customize your chat app through the chat.config file. The file syntax is as so:
```
chat:room1:my-name
geometry:500:500 
notifications:toast
```
The following will auto join you to the room names 'room1', with the name 'my-name'. 

The geometry is pretty self explanatory, I couldn't get the widgets to resize along with the window, so I made it from a config file. It defaults to 500x500.

The notifications option is for alerting you when a message arrives to your current room, if the chat window is minimized. The options are "toast", "tone", "none".  "toast" will display a windows desktop notification, "tone" will play a tone.wav file, and "none" will disable all notifications.

The ommition of a chat.config file will result in the following:

Joining the lobby as a default (You cannot chat in the lobby, it is simply a list of current rooms). To rejoin the lobby, click the "rooms" option in the 
"File" menu.

A name of ```anon-[random number (0-100)] ```

A geometry of 500x500

Tone notifications


dependenices:
```
pygame
urllib3
webbrowser
requests
```

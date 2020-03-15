# Audiohub
A simple project for remote audio playback. It is designed with a raspberry pi in mind, connected to an audio device that can be controlled through a web client.

**This project is meant to be deployed in an internal network. It is not recommended to be exposed to a public network.**

## Design
The core design of the project is a single flask application, installed on the desired device, that exposes a web client with functionality for playback (either for the internal storage or a mounted directory) or direct play from youtube. The communication between the web client and the backend is done in realtime using web sockets.

The flask app is built with Python 3 and uses the **flask-socketio** project for enabling the web socket interactions. 

The web client is a single page application built with angular.

The audio playback is achieved using a backend process with an audio playback program that allows headless control. Such programs are **mplayer**, **mpv**, **vlc** and more. For which program to be used, an appropriate setting needs to be set (see Configuration for more).

## Configuration
The project is built to be configurable. To achieve this a single json file holds all available settings that can be set. This settings are

1. **server**: This section contains entries for the ip address, port and flask secret of the application.
2. **database**: Sets the connection string to the sqlite database.
3. **youtube**: Specifies the path to the youtube-dl executable for both windows and linux.
4. **backend**: An array of backend programs that can be used for playback. This configuration will include the name, and path to the desired executable (for both windows and linux). All paths to the executable will be tested and the first one that exists will be set as the backend.

*A settings.json file is already present as an example in the server directory.*

## Building
For the backend the pipenv toolchain is used so, go to the server directory and follow the below instructions.

1. Install **pipenv** gloabally using `pip install pipenv` if the default python in your system is Python 3, otherwise run `python3 -m pip install pipenv`.
2. Install all packages in the Pipfile using the `pipenv install` command.
3. Use the `pipenv shell` command to access the newly created virtual environment for the project.
4. Execute `python server.py` to start the flask application.

The web client is built using the angular cli. Go to the client directory and follow the below instructions.

1. Install all packages using `npm install`,
2. Edit the proper environment typescript file for the desirect host and port that the backend is running.
3. Execute `npm start` to run the development server.

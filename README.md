## Overview

**Project Title**: QuizLink

**Project Description**: A set of Python programs that allows users to connect to a central server, chat, and answer quiz questions together that can be customized by the server host.

**Project Goals**: To further my understanding of simple networking by using Python socket libraries that uses a server and client program to connect and interact with each other.

## Instructions for Build and Use

To run the server:

1. Download the repository contents to your computer.
2. Ensure Python 3.13 is installed on your device.
3. Edit `questions.json` to include questions that you want players to interact with.
3. In a Terminal or Command Prompt window, navigate to the `server` folder.
4. Type `python server.py` to start the program.
5. If successful, the server will start at localhost on a set port. This can be customized in code if you so desire.

To join a server through the client program:

1. Download the repository contents to your computer.
2. Ensure Python 3.13 is installed on your device as well as the `pyreadline3` dependency.
3. In a Terminal or Command Prompt window, navigate to the `client` folder.
4. Type `python client.py` to start the program.
5. Follow the instructions to join a server, and if successful, enter a username.
6. Now you can chat and interact with the server!

The available commands for the client are:

- `/exit` - Disconnect from the server and close the program.
- `/scores` - View the current scoreboard.
- `/startgame` - Trigger a new quiz for all players. 

## Development Environment 

To recreate the development environment, you need the following software and/or libraries with the specified versions:

* Python 3.13
* pyreadline3
* Visual Studio Code

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [Python Socket Documentation](https://docs.python.org/3/library/socket.html)
* [GeeksForGeeks](https://www.geeksforgeeks.org/python/socket-programming-python/)
* [Python Socket Tutorial](https://docs.python.org/3/howto/sockets.html)

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Remove phantom ">" character after input
* [ ] Add additional questions
* [ ] Resolve bugs / desync issues

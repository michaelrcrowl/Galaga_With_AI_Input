# Galaga_With_AI_Input

## Overview

I set up this project for an outreach event to high school students.  I wanted the idea of AI to be accessible and fun to garner interest in the broader field of computer science.  As such, I used Google's [Teachable Machine](https://teachablemachine.withgoogle.com/train) to creat my model and incorporated it into a game of Galaga that I made using pygame.  My game will run constantly (with infinite lives and enemies respawning) and students will hold up signs to the camera to interface with the game.

The model is relatively small since you can only upload as many pictures as your browser has memory; therefore, each of my 4 classes contain 4000 pictures (dataset described later).

## Dependencies

The environment in which I created this project use the following:

- Python 3.10.8
- Visual Studio Code v1.82.1 (current as of 8 September 2023)
- Windows 10
- Webcam built into a laptop
- Python packages:
	- pythonGraph (a beginner student-friendly wrapper for pygame)
	- cv2
	- numpy
	- PIL
	- keras (for loading the model in the repo)
- Other packages that should be installed by default with Python:
	- time
	- random
	- math
	- multiprocessing

## Installation and Setup

- Install [Python 3.10.8](https://www.python.org/downloads/release/python-3108/)
	- See the various installation options at the bottom of the webpage
- Install the necessary packages.  For Windows in VS Code, use the Powershell terminal at the bottom of the screen.  If you don't see it when you open VS Code, you can find it with the "View" drop down menu and clicking "Terminal"; alternatively, you can press `Ctrl+/``
	- `py -m pip install numpy`
	- `py -m pip install cv2`
	- `py -m pip install pillow`
	- `py -m pip install keras`
	- `py -m pip install pythonGraph`
- Clone the repo
- To wherever you saved the repo, open the file in VS Code.  You can use the File dropdown menu or press `Ctrl+k` `Ctrl+o`.

## Running the program

Open "spiral3.py" as this contains the main code.  When you run the program, it will first load the model from "ml_model/keras_model.h5"; this may take a minute depending on your setup.  My computer does not have a GPU as part of making AI accessible to kids.  

After it loads the model, it will start your webcam, and then it will get to playing the game.  
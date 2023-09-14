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

## Dataset

AI models learn best with great variations in its training data, but this isn't a lesson about machine learning.  I used the [MIT Indoor Scenes](https://www.kaggle.com/datasets/itsahmad/indoor-scenes-cvpr-2019) dataset because I intend for all my outreach events to be indoors.  I could add outdoor background for more variation, but that's a time for another iteration of the model.

After downloading the dataset (contains about 15,000 images), I created the "imageOverlayForAIModel.py" file.  The overlay script takes the "arrow.png" and overlays it on the background images.  The program creates multiple processes to create and save the images faster.  Each process will create one class of images ("up", "left", "right"), which correlate to the instructions we want to give to the game of Galaga ("shoot", "move left", "move right").  For each background, the process will create 10 data points by choosing 2 scales (making the arrow smaller to represent holding it farther from the camera) and 5 locations on the image (to represent various places you can hold the arrow in the webcam).  Italso chooses a random rotation for each data point.

To summarize, for each background I produce 10 arrow overlays for each class, or 30 total. A current iteration of the model that's not ready yet will use all 15,000 images for a total of about 405,000 datapoints.  To accommodate the limits of browser memory when using Teachable Machine, the current model uses 4000 datapoints for each class, or 16,000 datapoints total.
# Real-Time Sign Language Detection and Translation

This project aims to detect and translate Ethiopian sign language gestures in real-time using LSTM Deep learning neural network. The application, built as a desktop app using Python Tkinter, captures live video from the camera, processes it to detect hand gestures using the MediaPipe library, and translates them into Amharic text.

## Features
- Real-time sign language detection and translation
- Desktop application built with Python Tkinter
- Uses a pre-trained deep learning model for gesture recognition
- Simple and intuitive user interface
- Works with any standard webcam

## Requirements
- Python 3.x
- Tkinter
- OpenCV
- NumPy
- Pillow (PIL)
- TensorFlow
- MediaPipe

## Installation
1. Clone this repository to your local machine.
2. Install the required Python packages by running `pip install -r requirements.txt`.
3. Run the application using `python main.py`.

## Usage
- Press the "Start Camera" button to begin capturing video from the webcam.
- Perform sign language gestures in front of the camera.
- The detected gestures will be translated into text and displayed on the screen.
- Press the "Stop Camera" button to stop capturing video.

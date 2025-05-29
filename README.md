## Object-Detection-Smart-Car

An AI-powered smart car that uses real-time object detection and voice feedback. Built with Raspberry Pi, YOLOv8, and gTTS.

## Project Overview

**Object-Detection-Smart-Car** is a Raspberry Pi-based robotic vehicle that uses a camera to detect objects in real-time. It leverages the YOLOv8 model for object detection and moves forward when it identifies a target object. Upon detecting a new object, it stops and provides a voice announcement in Turkish using gTTS.

## Features

* Real-time object detection using Raspberry Pi Camera
* YOLOv8 (`yolov8n.pt`) model from Ultralytics
* Voice alerts in Turkish using Google Text-to-Speech (gTTS)
* Moves forward when specific objects (e.g., person, car, animal) are detected
* Stops motors when no target is found
* Motor control using GPIO pins

## Technologies Used

* Python
* Raspberry Pi (GPIO BCM mode)
* Ultralytics YOLOv8
* OpenCV
* gTTS
* ffplay (for audio playback)

## Target Objects

The car responds to commonly encountered objects like:

```
person, car, dog, cat, bus, truck, bicycle, bottle, chair, laptop, etc.
```

You can find the full list of supported classes in the code under `TARGET_OBJECTS`.

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/Object-Detection-Smart-Car.git
   cd Object-Detection-Smart-Car
   ```

2. **Install dependencies:**

   ```bash
   pip install opencv-python numpy ultralytics gTTS
   ```

3. **Install ffmpeg (for ffplay):**

   ```bash
   sudo apt install ffmpeg
   ```

4. **Connect your motors and camera** to the Raspberry Pi using the correct GPIO pins defined in the code.

5. **Run the script:**

   ```bash
   python3 ypg.py
   ```

## License

This project is licensed under the Apache License 2.0.

## Contact

[aysezeynepaydogdu@gmail.com](mailto:aysezeynepaydogdu@gmail.com)

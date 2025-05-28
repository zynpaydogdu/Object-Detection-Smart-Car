from picamera2 import Picamera2
import cv2
import numpy as np
from ultralytics import YOLO
import RPi.GPIO as GPIO
import time
from gtts import gTTS
import os
import subprocess

model = YOLO("yolov8n.pt")

TARGET_OBJECTS = {
    'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck',
    'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench',
    'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra',
    'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
    'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove',
    'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
    'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange',
    'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
    'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse',
    'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
    'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier',
    'toothbrush'
}

# Motor pinleri
motor1_IN1, motor1_IN2, motor1_IN3, motor1_IN4 = 17, 27, 23, 24
motor1_ENA, motor1_ENB = 22, 25
motor2_IN1, motor2_IN2, motor2_IN3, motor2_IN4 = 5, 6, 13, 19
motor2_ENA, motor2_ENB = 12, 18

all_motor_pins = [
    motor1_IN1, motor1_IN2, motor1_IN3, motor1_IN4, motor1_ENA, motor1_ENB,
    motor2_IN1, motor2_IN2, motor2_IN3, motor2_IN4, motor2_ENA, motor2_ENB
]

GPIO.setmode(GPIO.BCM)
for pin in all_motor_pins:
    GPIO.setup(pin, GPIO.OUT)

def move_forward():
    GPIO.output(motor1_ENA, GPIO.HIGH)
    GPIO.output(motor1_ENB, GPIO.HIGH)
    GPIO.output(motor1_IN1, GPIO.HIGH)
    GPIO.output(motor1_IN2, GPIO.LOW)
    GPIO.output(motor1_IN3, GPIO.HIGH)
    GPIO.output(motor1_IN4, GPIO.LOW)
    GPIO.output(motor2_ENA, GPIO.HIGH)
    GPIO.output(motor2_ENB, GPIO.HIGH)
    GPIO.output(motor2_IN1, GPIO.HIGH)
    GPIO.output(motor2_IN2, GPIO.LOW)
    GPIO.output(motor2_IN3, GPIO.HIGH)
    GPIO.output(motor2_IN4, GPIO.LOW)

def stop_motors():
    for pin in all_motor_pins:
        GPIO.output(pin, GPIO.LOW)

def speak(text):
    filename = "nesne.mp3"
    if os.path.exists(filename):
        os.remove(filename)
    tts = gTTS(text=text, lang='tr')
    tts.save(filename)
    subprocess.run(["ffplay", "-nodisp", "-autoexit", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(filename)

picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()
time.sleep(1)

try:
    last_announced = ""
    while True:
        frame = picam2.capture_array()
        results = model(frame)
        found_target = False
        detected_label = ""

        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_id = int(box.cls[0])
                label = model.names[class_id]

                if label in TARGET_OBJECTS:
                    found_target = True
                    detected_label = label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, label, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        if found_target:
            move_forward()
            if detected_label != last_announced:
                stop_motors()
                speak(f"Bu bir {detected_label}")
                last_announced = detected_label
        else:
            stop_motors()

except KeyboardInterrupt:
    print("Klavye ile durduruldu.")
finally:
    picam2.stop()
    stop_motors()
    GPIO.cleanup()
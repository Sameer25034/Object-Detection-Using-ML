import streamlit as st
import cv2
import numpy as np
import time
import random
from helper import load_video_from_url, load_webcam, detect_objects

# Load YOLO
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))

st.title("🎥 Real-Time Object Detection")
option = st.radio("Choose input source:", ["Webcam", "YouTube URL"])

if option == "YouTube URL":
    url = st.text_input("Enter YouTube video URL:")
    if st.button("Start Detection"):
        cap = load_video_from_url(url)
        stframe = st.empty()
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = detect_objects(frame, net, output_layers, classes, colors)
            stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
        cap.release()

elif option == "Webcam":
    if st.button("Start Webcam"):
        cap = load_webcam()
        stframe = st.empty()
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = detect_objects(frame, net, output_layers, classes, colors)
            stframe.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB")
        cap.release()


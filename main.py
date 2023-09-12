import cv2
import datetime
import numpy as np
import tensorflow as tf
from object_detection.utils import visualization_utils as viz_utils
import pathlib
import tabulate
from typing import List, Tuple

import pygame
pygame.mixer.init()
ALARM_AUDIO_FILE_PATH = pathlib.Path('alarm.mp3')
pygame.mixer.music.load(ALARM_AUDIO_FILE_PATH)

# Load the model
model = tf.saved_model.load('efficientdet_d4_coco17_tpu-32/saved_model')
labels = pathlib.Path('efficientdet_d4_coco17_tpu-32/coco-labels-paper.txt').read_text().splitlines()
labels_map = {index+1: {"id": index+1, "name": label} for index,label in enumerate(labels)}


CONFIDENCE_THRESH = 0.3
WIDTH=1024
HEIGHT=576
OUTPUT_VIDEO_PATH = pathlib.Path('video.mp4')
FOURCC = cv2.VideoWriter_fourcc(*'mp4v')
OUTPUT_VIDEO = cv2.VideoWriter(str(OUTPUT_VIDEO_PATH), FOURCC, 1.5, (WIDTH,HEIGHT))
WHITE_COLOR = (255, 255, 255)

# Initialize the camera (usually 0 for the default camera, but it can be different)


def get_capture() -> cv2.VideoCapture:
    cv2.CAP_GSTREAMER
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
    return cap

cap = get_capture()

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

def detect_objects(image_np):
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]
    detections = model(input_tensor)
    return detections

def list_detected_elements(detections, confidence_thresh: float) -> List[Tuple[str, float]]:
    detected_classes = detections['detection_classes'][0].numpy().astype(np.int32)
    detected_scores = detections['detection_scores'][0].numpy()

    detection_data = np.array(['', 0])
    for index,class_id in enumerate(detected_classes):
        if class_id < len(labels) and detected_scores[index] > confidence_thresh:
            detection_data = np.vstack((detection_data, [labels[class_id-1], detected_scores[index].astype(float)]))

    return detection_data

def is_cat_detected(detections):
    detected_elements = list_detected_elements(detections, CONFIDENCE_THRESH)
    print(tabulate.tabulate(detected_elements[1:], headers=['Object', 'Confidence']))
    detected_elements = set(detected_elements[:, 0])
    return 'cell phone' in detected_elements
    #return 'cat' in detected_elements and 'person' not in detected_elements

cv2.namedWindow("Video Stream", cv2.WINDOW_NORMAL)

try:
    while True:
        # Capture a frame
        print('Capturing a frame...')
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        while not ret:
            print("Error: Could not read frame.")
            cap.release()
            cap = get_capture()
            ret, frame = cap.read()

        # Convert the frame to a NumPy array
        image_np = np.array(frame)

        detections = detect_objects(image_np)

        # Visualize and annotate the detected objects
        image_np_with_detections = cv2.cvtColor(image_np.copy(), cv2.COLOR_BGR2RGB)
        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'][0].numpy(),
            detections['detection_classes'][0].numpy().astype(np.int32),
            detections['detection_scores'][0].numpy(),
            labels_map,
            use_normalized_coordinates=True,
            max_boxes_to_draw=200,
            min_score_thresh=CONFIDENCE_THRESH
        )

        # Prepare for displaying
        image_np_with_detections = cv2.cvtColor(image_np_with_detections, cv2.COLOR_RGB2BGR)
        timestamp = datetime.datetime.now().strftime("%d.%m %H:%M:%S")
        cv2.putText(image_np_with_detections, timestamp, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, WHITE_COLOR, 2)

        # Display the annotated image
        if is_cat_detected(detections):
            print('Cat is in da hause!')
            OUTPUT_VIDEO.write(image_np_with_detections)
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play()
        else:
            pygame.mixer.music.stop()
            
        cv2.imshow("Video Stream", image_np_with_detections)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    OUTPUT_VIDEO.release()

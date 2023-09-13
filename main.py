import detector
import cv2
import numpy as np
import pathlib
import tabulate
import decorators
import video
import presenter
import image
import alarm

CONFIDENCE_THRESH = 0.3
WIDTH = 1024
HEIGHT = 576
WHITE_COLOR = (255, 255, 255)


# Load the model
detector.load_model(model_path=pathlib.Path('efficientdet_d4_coco17_tpu-32/saved_model'),
                    labels_path=pathlib.Path('efficientdet_d4_coco17_tpu-32/coco-labels-paper.txt'))
labels_map = detector.get_labels_map()

video.init(width=WIDTH, height=HEIGHT, fps=1.5)
image.init()
alarm.load(pathlib.Path('alarm.mp3'))

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

try:
    presenter.init()
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

        detections = detector.detect_objects(image_np)
        detected_elements = detector.list_detected_elements(
            detections, CONFIDENCE_THRESH)
        print(tabulate.tabulate(
            detected_elements[1:], headers=['Object', 'Confidence']))
        detected_elements = set(detected_elements[:, 0])

        # Visualize and annotate the detected objects
        decorated_frame = decorators.decorate_by_detections(image_np,detections,labels_map,CONFIDENCE_THRESH)
        decorators.decorate_by_timestamp(decorated_frame)

        # Display the annotated image
        if detector.is_detected(detections=detected_elements, musts=['cell phone']):
            print('Cat is in da hause!')
            video.write(decorated_frame)
            alarm.play_if_not_playing()
        else:
            alarm.stop()

        presenter.update(decorated_frame)
        image.update(decorated_frame)
except StopIteration:
    pass
finally:
    cap.release()
    presenter.release()
    video.release()

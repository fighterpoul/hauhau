import detector
import pathlib
import tabulate
import decorators
import video
import presenter
import image
import alarm
import camera

CONFIDENCE_THRESH = 0.3
WIDTH = 1024
HEIGHT = 576

detector.load_model(model_path=pathlib.Path('efficientdet_d4_coco17_tpu-32/saved_model'),
                    labels_path=pathlib.Path('efficientdet_d4_coco17_tpu-32/coco-labels-paper.txt'))
labels_map = detector.get_labels_map()

video.init(width=WIDTH, height=HEIGHT, fps=1.5)
image.init(image_path=pathlib.Path('./frame.jpg'))
alarm.load(pathlib.Path('alarm.mp3'))

with camera.create(width=WIDTH, height=HEIGHT) as camera_iterator:
    presenter.init()
    for frame in camera_iterator:
        try:
            detections = detector.detect_objects(frame)
            detected_elements = detector.list_detected_elements(
                detections, CONFIDENCE_THRESH)
            print(tabulate.tabulate(
                detected_elements[1:], headers=['Object', 'Confidence']))
            detected_elements = set(detected_elements[:, 0])

            decorated_frame = decorators.decorate_by_detections(
                frame, detections, labels_map, CONFIDENCE_THRESH)
            decorators.decorate_by_timestamp(decorated_frame)

            if detector.is_detected(detections=detected_elements, musts=['cell phone']):
                video.write(decorated_frame)
                alarm.play_if_not_playing()
            else:
                alarm.stop()

            presenter.update(decorated_frame)
            image.update(decorated_frame)
        except KeyboardInterrupt:
            break

presenter.release()
video.release()

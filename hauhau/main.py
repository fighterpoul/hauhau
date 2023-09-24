from hauhau import camera, alarm, image, presenter, video, decorators, detector

import os
import pathlib
import tabulate
from typing import Optional, Set
import time
import logging

detections_logger = logging.getLogger('hauhau-detections')
logger = logging.getLogger('hauhau')

def _init_modules(model_path: pathlib.Path,
                  labels_path: pathlib.Path,
                  frame_width: int, frame_height: int, fps: float,
                  videos_folder_path: Optional[pathlib.Path],
                  frame_image_path: Optional[pathlib.Path],
                  audio_alarm_path: pathlib.Path,
                  log_frame_detections: bool):
    detector.load_model(model_path=model_path,
                        labels_path=labels_path)

    if videos_folder_path:
        video.init(videos_folder_path=videos_folder_path, width=frame_width,
                   height=frame_height, fps=fps)

    if frame_image_path:
        image.init(image_path=frame_image_path)

    alarm.init(audio_alarm_path)

    detections_logger.setLevel(logging.INFO if log_frame_detections else logging.CRITICAL)


def main(model_path: pathlib.Path,
         labels_path: pathlib.Path,
         confidence_thresh: float,
         musts: Set[str], must_nots: Set[str],
         frame_width: int, frame_height: int, camera_id: any, fps: float,
         videos_folder_path: Optional[pathlib.Path],
         frame_image_path: Optional[pathlib.Path],
         audio_alarm_path: Optional[pathlib.Path],
         preview: bool,
         log_frame_detections: bool):

    _init_modules(model_path, labels_path,
                  frame_width, frame_height, fps,
                  videos_folder_path, frame_image_path, audio_alarm_path,
                  log_frame_detections)

    labels_map = detector.get_labels_map()

    try:
        with camera.create(width=frame_width, height=frame_height, camera_id=camera_id) as camera_iterator:
            presenter.init(preview)
            for frame in camera_iterator:
                try:
                    detections = detector.detect_objects(frame)
                    detected_elements = detector.list_detected_elements(
                        detections, confidence_thresh)
                    
                    if len(detected_elements):
                        detections_logger.info(os.linesep + tabulate.tabulate(
                            detected_elements, headers=['Object', 'Confidence']))
                        detected_elements = set(detected_elements[:, 0])

                        decorated_frame = decorators.decorate_by_detections(
                            frame, detections, labels_map, confidence_thresh)
                        decorators.decorate_by_timestamp(decorated_frame)

                        if detector.is_detected(detections=detected_elements, musts=musts, must_nots=must_nots):
                            logger.info('All conditions met, object(s) detected!')
                            video.write(decorated_frame)
                            alarm.play_if_not_playing()
                        else:
                            alarm.stop()
                    else:
                        decorated_frame = frame
                        decorators.decorate_by_timestamp(decorated_frame)

                    presenter.update(decorated_frame)
                    image.update(decorated_frame)
                except KeyboardInterrupt:
                    break
    except TimeoutError as e:
        logger.error(f'Camera could not yield first frame in given timeout: {e}')

    video.release()
    alarm.release()
    presenter.release()
    time.sleep(2)

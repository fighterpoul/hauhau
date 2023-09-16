import numpy as np
import datetime
import cv2
try:
    from object_detection.utils import visualization_utils as viz_utils
except:
    viz_utils = None

def decorate_by_detections(frame: np.array, detections, labels_map, confidence_thresh) -> np.array:
    if not viz_utils:
        return frame
    
    frame_with_detections = cv2.cvtColor(
        frame.copy(), cv2.COLOR_BGR2RGB)
    viz_utils.visualize_boxes_and_labels_on_image_array(
        frame_with_detections,
        detections['detection_boxes'][0].numpy(),
        detections['detection_classes'][0].numpy().astype(np.int32),
        detections['detection_scores'][0].numpy(),
        labels_map,
        use_normalized_coordinates=True,
        max_boxes_to_draw=200,
        min_score_thresh=confidence_thresh
    )
    return cv2.cvtColor(frame_with_detections, cv2.COLOR_RGB2BGR)


def decorate_by_timestamp(frame: np.array, dateformat: str = "%d.%m %H:%M:%S", color=(255, 255, 255)):
    timestamp = datetime.datetime.now().strftime(dateformat)
    cv2.putText(frame, timestamp, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

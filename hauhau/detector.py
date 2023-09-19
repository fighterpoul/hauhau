import pathlib
import tensorflow as tf
import numpy as np
from typing import List, Set, Tuple

_model = None
_labels = None


def load_model(model_path: pathlib.Path, labels_path: pathlib.Path):
    global _model, _labels
    _model = tf.saved_model.load(str(model_path.resolve()))
    _labels = labels_path.read_text().splitlines()


def get_labels_map() -> dict:
    global _labels
    return {index+1: {"id": index+1, "name": label} for index, label in enumerate(_labels)}


def detect_objects(image_np: np.array):
    input_tensor = tf.convert_to_tensor(image_np)
    input_tensor = input_tensor[tf.newaxis, ...]
    detections = _model(input_tensor)
    return detections


def list_detected_elements(detections, confidence_thresh: float) -> np.array:
    detected_classes = detections['detection_classes'][0].numpy().astype(
        np.int32)
    detected_scores = detections['detection_scores'][0].numpy()

    detection_data = np.array(['', 0])
    for index, class_id in enumerate(detected_classes):
        if class_id < len(_labels) and detected_scores[index] > confidence_thresh:
            detection_data = np.vstack(
                (detection_data, [_labels[class_id-1], detected_scores[index].astype(float)]))

    return detection_data


def is_detected(detections: Set[str], musts: Set[str], must_nots: Set[str] = set()) -> bool:
    is_required_visible = all(item in detections for item in musts)
    is_excluded_not_visible = not bool(set(detections) & set(must_nots))
    return is_required_visible and is_excluded_not_visible

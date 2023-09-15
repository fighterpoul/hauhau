import cv2
import numpy as np
import logging

logger = logging.getLogger("hauhau")

_preview = True

def init(preview: bool):
    global _preview
    _preview = preview
    if preview:
        logger.info("Press Q to exit.")
        cv2.namedWindow("Video Stream", cv2.WINDOW_NORMAL)


def update(frame: np.array):
    if _preview:
        cv2.imshow("Video Stream", frame)


def release():
    if _preview:
        cv2.destroyAllWindows()

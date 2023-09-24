import numpy as np
import pathlib
import cv2
import logging
from PIL import Image

logger = logging.getLogger('hauhau')

_image_path = None


def init(image_path: pathlib.Path):
    global _image_path
    _image_path = image_path
    if image_path:
        logger.info(f'Frames will be saved in {image_path.resolve()}')


def update(frame: np.array):
    global _image_path
    if _image_path:
        Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).save(_image_path)
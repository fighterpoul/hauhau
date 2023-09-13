import numpy as np
import pathlib
import cv2
from PIL import Image

_image_path = pathlib.Path('./frame.jpg')


def init(image_path: pathlib.Path = pathlib.Path('./frame.jpg')):
    global _image_path
    _image_path = image_path


def update(frame: np.array):
    Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).save(_image_path)
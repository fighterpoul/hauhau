import cv2
from typing import Iterator
import logging

logger = logging.getLogger('hauhau')

try:
    from picamera import PiCamera
    import picamera.array
    import time

    class PiCameraFrameIterator:
        def __init__(self, resolution=(640, 480), framerate=30):
            self.resolution = resolution
            self.framerate = framerate
            self.camera = None

        def __enter__(self):
            self.camera = PiCamera(
                resolution=self.resolution, framerate=self.framerate)
            self.camera.start_preview()
            time.sleep(2)  # Allow the camera to warm up
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            if self.camera is not None:
                self.camera.stop_preview()
                self.camera.close()
                self.camera = None

        def __iter__(self):
            return self

        def __next__(self):
            if self.camera is None:
                raise ValueError(
                    "CameraFrameIterator is not inside a 'with' block")

            with picamera.array.PiRGBArray(self.camera) as output:
                self.camera.capture(output, 'rgb')
                frame = output.array
                return frame
except Exception as e:
    logger.error(f'Not possible to use picamera: {e}')


class CVCameraFrameIterator:
    def __init__(self, width: int, height: int, camera_id=0):
        cv2.CAP_GSTREAMER
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.capture = None

    def __enter__(self):
        self.capture = cv2.VideoCapture(self.camera_id)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.capture is not None:
            self.capture.release()
            self.capture = None

    def __iter__(self):
        return self

    def __next__(self):
        if not self.capture.isOpened():
            logger.error('Video capture is not opened')
            raise StopIteration

        ret, frame = self.capture.read()

        if not ret:
            logger.error('Could not capture video frame. Finishing.')
            raise StopIteration
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.info('Bye')
            raise StopIteration

        return frame


def create(width: int, height: int, camera_id=0) -> Iterator:
    return CVCameraFrameIterator(width=width, height=height, camera_id=camera_id)

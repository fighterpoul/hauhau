import cv2
from typing import Iterator, Callable
import logging
import threading
import time
from queue import Queue

logger = logging.getLogger('hauhau')

try:
    from picamera import PiCamera
    import picamera.array

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


class LifoQueue():
    def __init__(self, max_size):
        self.queue = []
        self.max_size = max_size
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)

    def put(self, item):
        with self.mutex:
            self.queue.append(item)
            if len(self.queue) > self.max_size:
                self.queue.pop(0)
            self.not_empty.notify()

    def pop(self):
        with self.not_empty:
            while not len(self.queue):
                self.not_empty.wait(1)
            return self.queue.pop()

    def size(self):
        with self.mutex:
            return len(self.queue)

    def is_empty(self) -> bool:
        return self.size() <= 0
    
def wait_for_condition(predicate: Callable, timeout: int = 10, error_type=TimeoutError):
    """
    Wait for a condition to be True or raise an error if the timeout is exceeded.

    Args:
        predicate (callable): A function that returns True or False.
        timeout (float): The maximum time to wait for the condition to return True (in seconds).
        error_type (Exception, optional): The type of error to raise if the timeout is exceeded.
            Defaults to RuntimeError.

    Raises:
        error_type: If the condition is not met within the specified timeout.
    """
    start_time = time.time()

    while not predicate():
        elapsed_time = time.time() - start_time
        if elapsed_time >= timeout:
            raise error_type(f"Timeout exceeded ({timeout} seconds)")
        time.sleep(0.2)


class CVCameraFrameIterator:

    def __init__(self, width: int, height: int, camera_id=0):
        cv2.CAP_GSTREAMER
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.capture = None
        self.queue = LifoQueue(3)
        self.thread = threading.Thread(target=self.update, args=())
        self.thread.daemon = True

    def update(self):
        while self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                self.queue.put(frame)

    def __enter__(self):
        self.capture = cv2.VideoCapture(self.camera_id)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.capture.set(cv2.CAP_PROP_BUFFERSIZE, 5)

        self.thread.start()
        wait_for_condition(lambda: not self.queue.is_empty())

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

        last_frame = self.queue.pop()

        if last_frame is None:
            logger.error('Could not capture video frame. Finishing.')
            raise StopIteration
        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.info('Bye')
            raise StopIteration

        return last_frame


def create(width: int, height: int, camera_id=0) -> Iterator:
    return CVCameraFrameIterator(width=width, height=height, camera_id=camera_id)

import cv2

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
            self.camera = PiCamera(resolution=self.resolution, framerate=self.framerate)
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
                raise ValueError("CameraFrameIterator is not inside a 'with' block")

            with picamera.array.PiRGBArray(self.camera) as output:
                self.camera.capture(output, 'rgb')
                frame = output.array
                return frame
except:
    print('Not possible to use picamera')


class CVCameraFrameIterator:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.capture = None

    def __enter__(self):
        self.capture = cv2.VideoCapture(self.camera_id)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.capture is not None:
            self.capture.release()
            self.capture = None

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame = self.capture.read()
        if not ret:
            raise StopIteration
        if cv2.waitKey(1) & 0xFF == ord('q'):
            raise StopIteration
        return frame

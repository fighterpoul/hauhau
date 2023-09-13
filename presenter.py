import cv2
import numpy as np

def init():
    cv2.namedWindow("Video Stream", cv2.WINDOW_NORMAL)

def update(frame: np.array):
    cv2.imshow("Video Stream", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        raise StopIteration

def release():
    cv2.destroyAllWindows()
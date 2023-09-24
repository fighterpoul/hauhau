import pathlib
import datetime
import cv2
import numpy as np
import logging

logger = logging.getLogger('hauhau')

VIDEO_TIMESTAMP_FORMAT = "%Y-%m-%d"

_videos_folder_path = None

_writer = None
_width = None
_height = None
_fps = None
_current_file_path = None

def init(videos_folder_path: pathlib.Path, width: int, height: int, fps: float):
    global _writer, _width, _height, _fps, _videos_folder_path, _current_file_path
    _videos_folder_path = videos_folder_path
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    _current_file_path = get_supposed_filepath()
    _writer = cv2.VideoWriter(
        str(_current_file_path), fourcc, fps, (width, height))
    _width = width
    _height = height
    _fps = fps

def get_supposed_filepath() -> pathlib.Path:
    timestamp = datetime.datetime.now().strftime(VIDEO_TIMESTAMP_FORMAT)
    video_path = _videos_folder_path.joinpath(f'video-{timestamp}.mp4')
    counter = 0
    # because VideoWriter just overrides existing file instead of concatenating frames
    while video_path.is_file():
        video_path = _videos_folder_path.joinpath(f'video-{timestamp}-{counter}.mp4')
        counter += 1
    logger.info(f'Will write frames to {video_path.resolve()}')
    return video_path

def write(frame: np.array):
    global _writer, _current_file_path
    timestamp = datetime.datetime.now().strftime(VIDEO_TIMESTAMP_FORMAT)
    need_to_create_new_file = timestamp not in _current_file_path.name if _current_file_path else ''
    if need_to_create_new_file:
        logger.info(f'Recreating video file writter')
        _recreate()
    _writer.write(frame)

def release():
    global _writer
    if _writer:
        _writer.release()

def _recreate():
    global _width, _height, _fps, _videos_folder_path
    release()
    init(videos_folder_path=_videos_folder_path, width=_width, height=_height, fps=_fps)
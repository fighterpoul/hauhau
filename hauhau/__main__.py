import argparse
import pathlib
from hauhau.alarm import AUDIO_FILES_DIR


def _exiting_directory(value) -> pathlib.Path:
    dir = pathlib.Path(value)
    if not dir.is_dir():
        raise argparse.ArgumentError(
            f'{value} is not path to an existing directory')
    return dir


def _exiting_file(value) -> pathlib.Path:
    file = pathlib.Path(value)
    if not file.is_file():
        raise argparse.ArgumentError(
            f'{value} is not path to an existing file')
    return file


def _positive_int(value) -> int:
    try:
        integer = int(value)
        if integer <= 0:
            raise ValueError()
        return integer
    except:
        raise argparse.ArgumentError(
            f'{value} is not a positive integer')


def _positive_float(value) -> float:
    try:
        flt = float(value)
        if flt <= 0.0:
            raise ValueError()
        return flt
    except:
        raise argparse.ArgumentError(
            f'{value} is not a positive float')


def _percent(value) -> float:
    try:
        flt = float(value)
        if flt < 0.0 or flt > 1.0:
            raise ValueError()
        return flt
    except:
        raise argparse.ArgumentError(
            f'{value} is not a float representing percents (not in range 0.0-1.0)')


def main():

    parser = argparse.ArgumentParser(
        description='Get them spotted!', prog="hauhau")
    parser.add_argument('--tf-model', type=_exiting_directory,
                        help='Path to a directory with a TensorFlow model (*.pb).', required=True)
    parser.add_argument('--model-labels', type=_exiting_file,
                        help='Path to a text file with class labels. It will be used to map class IDs returned by tf-model to human-readable labels.', required=True)
    parser.add_argument('--confidence-threshold', type=_percent, default=0.3,
                        help='How confident the model must be about detected musts and must_nots to consider them as visible on camera.')

    parser.add_argument('--musts', type=str, nargs='+', default='cat',
                        help='Objects that must be visible on camera for alarm to be raised. "Cat" by default.')
    parser.add_argument('--must-nots', type=str, nargs='*', default='person',
                        help='Objects that must NOT be visible on camera for alarm to be raised. "Person" by default.')

    parser.add_argument('--frame-width', type=_positive_int,
                        help='Width of a frame captured by camera', required=True)
    parser.add_argument('--frame-height', type=_positive_int,
                        help='Height of a frame captured by camera', required=True)
    parser.add_argument('--camera-id', default=0,
                        help='Camera Id. You can provide everything acceptable for cv2.VideoCapture.')

    parser.add_argument('--alarm-sound', type=_exiting_file,
                        help='Path to an alarm audio file.', default=AUDIO_FILES_DIR.joinpath('barking.mp3'))
    parser.add_argument('--wall-of-shame', type=_exiting_directory,
                        help='Optional. Path to a directory where video recordings will be published. If furry gets spotted, here are your proofs.')
    parser.add_argument('--fps', type=_positive_float, default=1,
                        help='Fps of videos published on wall of shame, thus required if wall of shame is provided. Depends on host\'s performance, usually something around 1fps.')
    parser.add_argument('--last-frame-path', type=pathlib.Path,
                        help='Optional. Path to a file that will be continuously updated by last frame with detections. Can be used i.e. to webstream by using ffmpeg.')

    parser.add_argument('--preview', action=argparse.BooleanOptionalAction,
                        help='Will display window with camera preview')
    parser.add_argument('--log-frame-detections',
                        action=argparse.BooleanOptionalAction, help='Will log detected objects.')

    args = parser.parse_args()

    from hauhau.main import main as hauhau_main
    hauhau_main(
        model_path=args.tf_model,
        labels_path=args.model_labels,
        confidence_thresh=args.confidence_threshold,
        musts=set(args.musts),
        must_nots=set(args.must_nots),
        frame_width=args.frame_width,
        frame_height=args.frame_height,
        camera_id=args.camera_id,
        fps=args.fps,
        videos_folder_path=args.wall_of_shame,
        frame_image_path=args.last_frame_path,
        audio_alarm_path=args.alarm_sound,
        preview=args.preview,
        log_frame_detections=args.log_frame_detections
    )


if __name__ == "__main__":
    main()

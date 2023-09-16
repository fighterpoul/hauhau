# WIP - still in early alpha!!!

# `hauhau` - The "No More Table Cat" Alert

## What's hauhau?
**hauhau** is an echoism for barking sound in Polish. But thanks to this package it's a way more!
`hauhau` is your feline-enforcement companion! It's a snazzy Python tool that uses TensorFlow magic to keep your kitty off the kitchen table. When our furry friends break the rules, `hauhau` barks (well, not literally) and sends them running!
`hauhau` is proven working on Linux and Raspberry Pi (`picamera`).

## Quick Setup

1. Install Python >=3.10 if you haven't already.

2. Get TensorFlow models and file with class labels.
I get it working by running:
```bash
sudo apt install protobuf-compiler

git clone https://github.com/tensorflow/models.git

cd models/research/

protoc object_detection/protos/*.proto --python_out=.

cp object_detection/packages/tf2/setup.py .

pip install .
```

3. Get `hauhau` with this simple command:

```bash
git clone https://github.com/fighterpoul/hauhau.git
cd hauhau
# provide correct path to your TensorFlow model and txt with labels - Here is model that put my furry into trouble!
python -m hauhau \
    --tf-model=efficientdet_d4_coco17_tpu-32/saved_model \
    --model-labels=efficientdet_d4_coco17_tpu-32/coco-labels-paper.txt \
    --frame-width=1024 --frame-height=576
```

## Customization - More Than Just Cat Control!

`hauhau` is super flexible! While it's perfect for cat-wrangling, you can customize it for all sorts of scenarios. For instance, keep an eye on your kids eating sweets while you're not around. Want to know if someone's raiding the cookie jar? `hauhau`'s got your back!

## Advanced

```bash
>_ python -m hauhau --help

usage: hauhau [-h] --tf-model TF_MODEL --model-labels MODEL_LABELS
              [--confidence-threshold CONFIDENCE_THRESHOLD]
              [--musts MUSTS [MUSTS ...]] [--must-nots [MUST_NOTS ...]]
              --frame-width FRAME_WIDTH --frame-height FRAME_HEIGHT
              [--alarm-sound ALARM_SOUND] [--wall-of-shame WALL_OF_SHAME]
              [--fps FPS] [--last-frame-path LAST_FRAME_PATH]
              [--preview | --no-preview]
              [--log-frame-detections | --no-log-frame-detections]

Get them spotted!

options:
  -h, --help            show this help message and exit
  --tf-model TF_MODEL   Path to a directory with a TensorFlow model (*.pb).
  --model-labels MODEL_LABELS
                        Path to a text file with class labels. It will be used to
                        map class IDs returned by tf-model to human-readable
                        labels.
  --confidence-threshold CONFIDENCE_THRESHOLD
                        How confident the model must be about detected musts and
                        must_nots to consider them as visible on camera.
  --musts MUSTS [MUSTS ...]
                        Objects that must be visible on camera for alarm to be
                        raised. "Cat" by default.
  --must-nots [MUST_NOTS ...]
                        Objects that must NOT be visible on camera for alarm to be
                        raised. "Person" by default.
  --frame-width FRAME_WIDTH
                        Width of a frame captured by camera
  --frame-height FRAME_HEIGHT
                        Height of a frame captured by camera
  --alarm-sound ALARM_SOUND
                        Path to an alarm audio file.
  --wall-of-shame WALL_OF_SHAME
                        Optional. Path to a directory where video recordings will
                        be published. If furry gets spotted, here are your proofs.
  --fps FPS             Fps of videos published on wall of shame, thus required if
                        wall of shame is provided. Depends on host's performance,
                        usually something around 1fps.
  --last-frame-path LAST_FRAME_PATH
                        Optional. Path to a file that will be continuously updated
                        by last frame with detections. Can be used i.e. to
                        webstream by using ffmpeg.
  --preview, --no-preview
                        Will display window with camera preview
  --log-frame-detections, --no-log-frame-detections
                        Will log detected objects.
```

TODO
```bash
sudo apt install v4l-utils
$ v4l2-ctl -d /dev/video0 --list-formats-ext

ffmpeg -re -framerate 1 -loop 1 -i frame.jpg -vf "format=yuv420p" -f mpegts -r 1 udp://localhost:1234
ffplay udp://localhost:1234
```

## Kudos
All default sounds downloaded from pixabay.com - awesome place with Royalty-free assets.
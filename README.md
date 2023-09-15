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
TODO
```bash
sudo apt install v4l-utils
$ v4l2-ctl -d /dev/video0 --list-formats-ext

ffmpeg -re -framerate 1 -loop 1 -i frame.jpg -vf "format=yuv420p" -f mpegts -r 1 udp://localhost:1234
ffplay udp://localhost:1234
```
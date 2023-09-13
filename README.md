git clone https://github.com/tensorflow/models.git

cd models/research/

sudo apt  install protobuf-compiler

protoc object_detection/protos/*.proto --python_out=.

cp object_detection/packages/tf2/setup.py .

pip install .


sudo apt install v4l-utils
$ v4l2-ctl -d /dev/video0 --list-formats-ext

ffmpeg -re -framerate 1 -loop 1 -i frame.jpg -vf "format=yuv420p" -f mpegts -r 1 udp://localhost:1234
ffplay udp://localhost:1234
#!/bin/sh

docker pull quay.io/mpuels/docker-py-kaldi-asr-and-model:kaldi-generic-en-tdnn_sp-r20180815
docker run --rm -p 127.0.0.1:8080:80/tcp quay.io/mpuels/docker-py-kaldi-asr-and-model:kaldi-generic-en-tdnn_sp-r20180815 &
docker_pid=$!

python kaldi.py

kill $docker_pid
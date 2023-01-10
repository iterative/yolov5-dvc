#!/usr/bin/env bash

export USER_ID=$(id -u)

docker build\
    -t yolov5-dvc:latest \
    --build-arg USER_ID=${USER_ID} \
    .

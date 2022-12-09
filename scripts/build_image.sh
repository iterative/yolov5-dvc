#!/usr/bin/env bash

export USER_ID=$(id -u)

docker build\
    -t openbot-vision-object-detection:latest \
    --build-arg USER_ID=${USER_ID} \
    .

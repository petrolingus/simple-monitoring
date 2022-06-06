#!/bin/bash

REPOSITORY_NAME="petrolingus/simple-monitoring:latest"
BUILD_DIR="build"

cd $(dirname "$0")

cp main.py ${BUILD_DIR}/main.py

docker build -t ${REPOSITORY_NAME} --no-cache --network=host ${BUILD_DIR}

for id in ${DOCKER_NAMES}; do
  docker tag ${REPOSITORY_NAME} "$id"
done

docker push ${REPOSITORY_NAME}
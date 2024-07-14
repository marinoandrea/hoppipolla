#!/bin/sh

PROTOS_FOLDER="./hoppipolla/protos" 

poetry run python -m grpc_tools.protoc \
    -I../../protos \
    --python_out=$PROTOS_FOLDER \
    --pyi_out=$PROTOS_FOLDER \
    --grpc_python_out=$PROTOS_FOLDER \
    ../../protos/*.proto
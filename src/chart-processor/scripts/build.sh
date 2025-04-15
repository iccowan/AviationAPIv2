#!/bin/sh

ABS_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $ABS_PATH/..

if [ -d "build" ]; then rm -rf "build"; fi
if [ -f "build.zip" ]; then rm -f "build.zip"; fi

mkdir build

pip install -t build -r requirements.txt --platform manylinux2014_x86_64 --only-binary=:all:
find app -name '*.py' -exec rsync -R {} build \;


#!/bin/sh

ABS_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_PATH=$ABS_PATH/..

MODULE="$1"
BUILD_NUMBER="${BUILD_NUMBER}"

if [ "$MODULE" = "" ]; then
    echo "Please specify module"
    exit 1
fi

if [ "$BUILD_NUMBER" = "" ]; then
    BUILD_NUMBER="0"
fi

MODULE_PATH=$PROJECT_PATH/$MODULE

if [ -d "$MODULE_PATH/build" ]; then rm -rf $MODULE_PATH/build; fi
if [ -f "$MODULE_PATH/build.zip" ]; then rm -f $MODULE_PATH/build.zip; fi

mkdir $MODULE_PATH/build
mkdir $MODULE_PATH/build/aviationapi

cp -r $PROJECT_PATH/lib $MODULE_PATH/build/aviationapi/.
cd $MODULE_PATH
find app -name '*.py' -exec rsync -R {} "$MODULE_PATH/build/aviationapi/$MODULE" \;
cd $PROJECT_PATH

pip install -t $MODULE_PATH/build -r $PROJECT_PATH/requirements.txt --platform manylinux2014_x86_64 --only-binary=:all:


PRESENT_PATH="$(pwd)"
cd $MODULE_PATH/build
zip -r ../build.zip .
cd $PRESENT_PATH

rm -r $MODULE_PATH/build

BUILD_NAME=$(echo "$MODULE" | tr "_" "-")
aws s3 mv $MODULE_PATH/build.zip "s3://${S3_BUCKET_NAME}/$BUILD_NAME-$BUILD_NUMBER.zip"

echo "build-name=$BUILD_NAME-$BUILD_NUMBER" >> $GITHUB_OUTPUT

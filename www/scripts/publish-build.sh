#!/bin/sh

ABS_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_PATH=$ABS_PATH/..

BUILD_NUMBER="${BUILD_NUMBER}"

if [ "$BUILD_NUMBER" = "" ]; then
    BUILD_NUMBER="0"
fi

if [ -f "$PROJECT_PATH/build.zip" ]; then rm -f $PROJECT_PATH/build.zip; fi

cd $PROJECT_PATH/build
zip -r ../build.zip .
cd $PROJECT_PATH

rm -r $PROJECT_PATH/build

BUILD_NAME="www"
aws s3 mv $PROJECT_PATH/build.zip "s3://${S3_BUCKET_NAME}/$BUILD_NAME-$BUILD_NUMBER.zip"

echo "build-name=$BUILD_NAME-$BUILD_NUMBER" >> $GITHUB_OUTPUT

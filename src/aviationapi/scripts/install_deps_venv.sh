#!/bin/sh

ABS_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_PATH=$ABS_PATH/..

MODULE="$1"

if [ "$MODULE" = "" ]; then
    echo "Please specify module"
    exit 1
fi

MODULE_PATH=$PROJECT_PATH/$MODULE
cd $MODULE_PATH

. $PROJECT_PATH/scripts/activate_venv.sh $MODULE_NAME

pip3 install -r $PROJECT_PATH/requirements.txt -r $PROJECT_PATH/requirements.ci.txt -r $MODULE_PATH/requirements.txt

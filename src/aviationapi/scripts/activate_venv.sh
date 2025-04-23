#!/bin/sh

ABS_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
PROJECT_PATH=$ABS_PATH/..

MODULE="$1"

if [ "$MODULE" = "" ]; then
    echo "Please specify module"
    exit 1
fi

MODULE_PATH=$PROJECT_PATH/$MODULE

source $MODULE_PATH/.venv/bin/activate


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

rm -rf .venv

python3 -m venv .venv --prompt "$MODULE"

. $PROJECT_PATH/scripts/activate_venv.sh $MODULE_NAME

pip3 install --upgrade pip

. $PROJECT_PATH/scripts/install_deps_venv.sh $MODULE_NAME


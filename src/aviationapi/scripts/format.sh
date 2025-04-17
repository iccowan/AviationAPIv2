#!/bin/sh

ABS_PATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
cd $ABS_PATH/..

DIRS="."
CHECK_ONLY=0
EXIT_CODE=0

if [ "$1" = "-c" ]; then
    CHECK_ONLY=1
fi

if [ "$CHECK_ONLY" = "1" ]; then
    autoflake -c -r -v --in-place --remove-unused-variables $DIRS
    EXIT_CODE=$(( EXIT_CODE + $? ))
    echo ""
    isort $DIRS -c -v
    EXIT_CODE=$(( EXIT_CODE + $? ))
    echo ""
    black $DIRS --check
    EXIT_CODE=$(( EXIT_CODE + $? ))
else
    autoflake -r -v --in-place --remove-unused-variables $DIRS
    echo ""
    isort $DIRS -v
    echo ""
    black $DIRS
fi

exit $EXIT_CODE


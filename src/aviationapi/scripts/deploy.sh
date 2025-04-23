#!/bin/sh

aws lambda update-function-code \
    --function-name "${LAMBDA_FUNCTION_NAME}" \
    --s3-bucket "${S3_BUCKET_NAME}" \
    --s3-key "${BUILD_NAME}.zip" \
    --no-cli-pager


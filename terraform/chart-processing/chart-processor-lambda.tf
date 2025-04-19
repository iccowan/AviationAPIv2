data "archive_file" "lambda-archive" {
  type        = "zip"
  source_dir  = var.SOURCE_DIR
  output_path = var.OUTPUT_PATH
}

resource "aws_lambda_function" "aviationapi-chart-processor-lambda" {
  function_name = "aviationapi-chart-processor"

  runtime     = var.PY_VERSION
  memory_size = 3008
  timeout     = 360

  filename         = var.OUTPUT_PATH
  handler          = "aviationapi.chart_processor.app.lambda_function.lambda_handler"
  source_code_hash = data.archive_file.lambda-archive.output_base64sha256

  role = aws_iam_role.chart-processor-lambda-role.arn

  ephemeral_storage {
    size = 3072
  }

  environment {
    variables = {
      DOWNLOAD_PATH                          = "/tmp"
      S3_BUCKET_NAME                         = var.S3_BUCKET.bucket
      UPLOAD_THREADS                         = 100
      CHART_BASE_URL                         = var.CHARTS_BASE_URL
      AIRPORTS_TABLE_NAME                    = var.AIRPORTS_TABLE.name
      TRIGGER_CHART_POST_PROCESSOR_TOPIC_ARN = var.TRIGGER_CHART_POST_PROCESSOR_TOPIC.arn
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_role" "chart-processor-lambda-role" {
  name = "chart-processor-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = ["sts:AssumeRole"],
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "lambda-chart-processor-role" {
  name = "chart-processor-lambda-role-policy"
  role = aws_iam_role.chart-processor-lambda-role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "S3PutObject"
        Effect   = "Allow"
        Action   = "s3:PutObject",
        Resource = "${var.S3_BUCKET.arn}/*"
      },
      {
        Sid    = "WriteTable"
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem"
        ],
        Resource = [
          var.AIRPORTS_TABLE.arn
        ]
      },
      {
        Sid    = "PublishMessage",
        Effect = "Allow",
        Action = [
          "sns:Publish"
        ],
        Resource = [
          var.TRIGGER_CHART_POST_PROCESSOR_TOPIC.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda-chart-processor" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.chart-processor-lambda-role.name
}


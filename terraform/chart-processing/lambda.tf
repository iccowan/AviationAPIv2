data "archive_file" "api_lambda" {
  type        = "zip"
  source_dir  = var.SOURCE_DIR
  output_path = var.OUTPUT_PATH
}

resource "aws_lambda_function" "aviationapi_chart_processor_lambda" {
  function_name = "aviationapi-api-chart-processor"

  runtime     = var.PY_VERSION
  memory_size = 3008
  timeout     = 360

  filename         = var.OUTPUT_PATH
  handler          = "app.chart-processor.lambda_handler"
  source_code_hash = data.archive_file.api_lambda.output_base64sha256

  role = aws_iam_role.chart_processor_lambda_role.arn

  ephemeral_storage {
    size = 2048
  }

  environment {
    variables = {
      DOWNLOAD_PATH = "/tmp"
      S3_BUCKET_NAME = var.S3_BUCKET.bucket
      UPLOAD_THREADS = 100
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_role" "chart_processor_lambda_role" {
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

resource "aws_iam_role_policy" "lambda_chart_processor_role" {
  name = "chart-processor-lambda-role-policy"
  role = aws_iam_role.chart_processor_lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow",
        Action   = "s3:ListBucket"
        Resource = var.S3_BUCKET.arn
      },
      {
        Effect   = "Allow"
        Action   = "s3:PutObject",
        Resource = "${var.S3_BUCKET.arn}/*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda-chart-processor" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.chart_processor_lambda_role.name
}


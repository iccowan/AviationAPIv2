data "archive_file" "lambda-archive" {
  type        = "zip"
  source_dir  = var.SOURCE_DIR
  output_path = var.OUTPUT_PATH
}

resource "aws_lambda_function" "aviationapi-chart-pre-processor-lambda" {
  function_name = "aviationapi-chart-pre-processor"

  runtime     = var.PY_VERSION
  memory_size = 256
  timeout     = 10

  filename         = var.OUTPUT_PATH
  handler          = "app.chart_pre_processor.lambda_handler"
  source_code_hash = data.archive_file.lambda-archive.output_base64sha256

  role = aws_iam_role.chart-pre-processor-lambda-role.arn

  environment {
    variables {
      TRIGGER_CHART_PROCESSOR_TOPIC_ARN = var.TRIGGER_CHART_PROCESSOR_TOPIC.arn
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_role" "chart-pre_processor-lambda-role" {
  name = "chart-pre-processor-lambda-role"

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

resource "aws_iam_role_policy" "lambda-chart-pre-processor-role" {
  name = "chart-pre-processor-lambda-role-policy"
  role = aws_iam_role.chart-pre-processor-lambda-role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "GetWriteDeleteTable"
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:DeleteItem"
        ],
        Resource = [
          var.AIRAC_TABLE.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda-chart-pre-processor" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.chart-pre-processor-lambda-role.name
}

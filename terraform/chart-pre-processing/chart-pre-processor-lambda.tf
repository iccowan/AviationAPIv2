resource "aws_lambda_function" "aviationapi-chart-pre-processor-lambda" {
  function_name = "aviationapi-chart-pre-processor"

  runtime     = var.PY_VERSION
  memory_size = 256
  timeout     = 10

  filename = var.INIT_LAMBDA
  handler  = "aviationapi.chart_pre_processor.app.lambda_function.lambda_handler"

  role = aws_iam_role.chart-pre-processor-lambda-role.arn

  environment {
    variables = {
      TRIGGER_CHART_PROCESSOR_TOPIC_ARN = var.TRIGGER_CHART_PROCESSOR_TOPIC.arn
      AIRAC_TABLE_NAME                  = var.AIRAC_TABLE.name
    }
  }
}

resource "aws_iam_role" "chart-pre-processor-lambda-role" {
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
      },
      {
        Sid    = "PublishMessage",
        Effect = "Allow",
        Action = [
          "sns:Publish"
        ],
        Resource = [
          var.TRIGGER_CHART_PROCESSOR_TOPIC.arn
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda-chart-pre-processor" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.chart-pre-processor-lambda-role.name
}

resource "aws_lambda_function" "aviationapi-chart-post-processor-lambda" {
  function_name = "aviationapi-chart-post-processor"

  runtime                        = var.PY_VERSION
  reserved_concurrent_executions = 1
  memory_size                    = 256
  timeout                        = 10

  filename = var.INIT_LAMBDA
  handler  = "aviationapi.chart_post_processor.app.lambda_function.lambda_handler"

  role = aws_iam_role.chart-post-processor-lambda-role.arn

  environment {
    variables = {
      AIRAC_TABLE_NAME = var.AIRAC_TABLE.name
    }
  }
}

resource "aws_iam_role" "chart-post-processor-lambda-role" {
  name = "chart-post-processor-lambda-role"

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

resource "aws_iam_role_policy" "lambda-chart-post-processor-role" {
  name = "chart-post-processor-lambda-role-policy"
  role = aws_iam_role.chart-post-processor-lambda-role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "WriteTable"
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem"
        ],
        Resource = [
          var.AIRAC_TABLE.arn
        ]
      },
      {
        Sid    = "QueryIndex"
        Effect = "Allow"
        Action = [
          "dynamodb:Query"
        ],
        Resource = [
          "${var.AIRAC_TABLE.arn}/index/${var.AIRAC_CYCLE_CHART_TYPE_INDEX_NAME}"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda-chart-post-processor" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.chart-post-processor-lambda-role.name
}

data "archive_file" "lambda-archive" {
  type        = "zip"
  source_dir  = var.SOURCE_DIR
  output_path = var.OUTPUT_PATH
}

resource "aws_lambda_function" "aviationapi-api-lambda" {
  function_name = "aviationapi-api"

  handler     = "app.main.handler"
  runtime     = var.PY_VERSION
  memory_size = 256
  timeout     = 10

  filename         = var.OUTPUT_PATH
  source_code_hash = data.archive_file.lambda-archive.output_base64sha256

  role = aws_iam_role.aviationapi-api-lambda-role.arn

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_iam_role" "aviationapi-api-lambda-role" {
  name = "aviapionapi-api-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "aviationapi-api-lambda" {
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
  role       = aws_iam_role.aviationapi-api-lambda-role.name
}

resource "aws_lambda_permission" "aviationapi-api-with-apigateway" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aviationapi-api-lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_api_gateway_rest_api.aviationapi-api-apigateway.execution_arn}/*/*"
}

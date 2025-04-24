output "trigger-chart-processor-topic" {
  value = aws_sns_topic.trigger-chart-processor
}

output "lambda-function" {
  value = aws_lambda_function.aviationapi-chart-processor-lambda
}

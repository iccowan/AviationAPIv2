output "trigger-chart-post-processor-topic" {
  value = aws_sns_topic.trigger-chart-post-processor
}

output "lambda-function" {
  value = aws_lambda_function.aviationapi-chart-post-processor-lambda
}

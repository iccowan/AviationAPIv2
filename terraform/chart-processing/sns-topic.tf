resource "aws_sns_topic" "trigger-chart-processor" {
  name = "trigger-chart-processor"
}

resource "aws_sns_topic_subscription" "trigger-chart-processor" {
  topic_arn = aws_sns_topic.trigger-chart-processor.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.aviationapi-chart-processor-lambda.arn
}

resource "aws_lambda_permission" "aviationapi-chart-processor-with-sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aviationapi-chart-processor-lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.trigger-chart-processor.arn
}


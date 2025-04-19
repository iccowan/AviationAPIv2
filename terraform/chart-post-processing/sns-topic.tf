resource "aws_sns_topic" "trigger-chart-post-processor" {
  name = "trigger-chart-post-processor"
}

resource "aws_sns_topic_subscription" "trigger-chart-post-processor" {
  topic_arn = aws_sns_topic.trigger-chart-post-processor.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.aviationapi-chart-post-processor-lambda.arn
}

resource "aws_lambda_permission" "aviationapi-chart-post-processor-with-sns" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aviationapi-chart-post-processor-lambda.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.trigger-chart-post-processor.arn
}



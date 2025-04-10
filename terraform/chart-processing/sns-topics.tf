resource "aws_sns_topic" "trigger_chart_processor" {
  name = "trigger-chart-processor"
}

resource "aws_sns_topic_subscription" "trigger_chart_processor" {
  topic_arn = aws_sns_topic.trigger_chart_processor.arn
  protocol = "lambda"
  endpoint = aws_lambda_function.aviationapi_chart_processor_lambda.arn
}

resource "aws_lambda_permission" "aviationapi_chart_processor_with_sns" {
  statement_id = "AllowExecutionFromSNS"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aviationapi_chart_processor_lambda.function_name
  principal = "sns.amazonaws.com"
  source_arn = aws_sns_topic.trigger_chart_processor.arn
}


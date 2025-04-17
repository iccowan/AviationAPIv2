resource "aws_cloudwatch_event_rule" "aviationapi-chart-pre-processor-trigger" {
  name = "aviationapi-chart-pre-processor-trigger"
  schedule_expression = "cron(17 4 * * ? *)"
  state = "DISABLED"
}

resource "aws_cloudwatch_event_target" "aviationapi-chart-pre-processor-trigger" {
  rule = aws_cloudwatch_event_rule.aviationapi-chart-pre-processor-trigger.name
  target_id = "lambda"
  arn = aws_lambda_function.aviationapi-chart-pre-processor-lambda.arn
}

resource "aws_lambda_permission" "aviationapi-charts-pre-processor-with-event" {
  statement_id = "AllowExecutionFromCloudWatch"
  action = "lambda:InvokeFunction"
  function_name = aws_lambda_function.aviationapi-chart-pre-processor-lambda.function_name
  principal = "events.amazonaws.com"
  source_arn = aws_cloudwatch_event_rule.aviationapi-chart-pre-processor-trigger.arn
}


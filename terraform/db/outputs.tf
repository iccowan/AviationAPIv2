output "aviationapi-airports-table-arn" {
  value = aws_dynamodb_table.aviationapi-airports-table.arn
}

output "aviationapi-airac-table-arn" {
  value = aws_dynamodb_table.aviationapi-airac-table.arn
}

output "aviationapi-airports-table" {
  value = aws_dynamodb_table.aviationapi-airports-table
}

output "aviationapi-airac-table" {
  value = aws_dynamodb_table.aviationapi-airac-table
}

output "aviationapi-airac-table-airac-cycle-chart-type-index-name" {
  value = var.AIRAC_CYCLE_CHART_TYPE_INDEX_NAME
}

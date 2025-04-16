resource "aws_dynamodb_table" "aviationapi-airac-table" {
  name                        = "aviationapi-airac"
  billing_mode                = "PAY_PER_REQUEST"
  hash_key                    = "cycle_type"
  range_key                   = "cycle_chart_type"
  deletion_protection_enabled = true

  attribute {
    name = "cycle_type"
    type = "S"
  }

  attribute {
    name = "cycle_chart_type"
    type = "S"
  }
}

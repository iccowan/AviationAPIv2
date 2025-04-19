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

  attribute {
    name = "airac"
    type = "S"
  }

  global_secondary_index {
    name            = var.AIRAC_CYCLE_CHART_TYPE_INDEX_NAME
    hash_key        = "airac"
    range_key       = "cycle_chart_type"
    projection_type = "ALL"
  }
}

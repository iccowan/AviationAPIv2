resource "aws_dynamodb_table" "aviationapi-airac-table" {
  name                        = "aviationapi-airac"
  billing_mode                = "PAY_PER_REQUEST"
  hash_key                    = "cycle_status"
  range_key                   = "airac_data_type"
  deletion_protection_enabled = true

  attribute {
    name = "cycle_status"
    type = "S"
  }

  attribute {
    name = "airac_data_type"
    type = "S"
  }
}

resource "aws_dynamodb_table" "aviationapi-airports-table" {
  name                        = "aviationapi-airports"
  billing_mode                = "PAY_PER_REQUEST"
  hash_key                    = "unique_airport_id"
  range_key                   = "chart_type::airac"
  deletion_protection_enabled = true

  attribute {
    name = "unique_airport_id"
    type = "S"
  }

  attribute {
    name = "chart_type::airac"
    type = "S"
  }

  ttl {
    attribute_name = "expire_at"
    enabled        = true
  }
}

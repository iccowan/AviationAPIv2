resource "aws_dynamodb_table" "aviationapi-airports-table" {
  name         = "aviationapi-airports"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "unique_airport_id"

  attribute {
    name = "unique_airport_id"
    type = "S"
  }
}

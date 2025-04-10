resource "aws_dynamodb_table" "aviationapi-airports-table" {
  name         = "aviationapi-airports"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "airport_icao"

  attribute {
    name = "airport_icao"
    type = "S"
  }
}

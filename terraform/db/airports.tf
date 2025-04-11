resource "aws_dynamodb_table" "aviationapi-airports-table" {
  name         = "aviationapi-airports"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "icao_ident"

  attribute {
    name = "icao_ident"
    type = "S"
  }
}

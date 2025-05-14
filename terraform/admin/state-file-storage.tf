resource "aws_s3_bucket" "aviationapi-terraform-state" {
  bucket = "aviationapi-terraform-state"
}

resource "aws_dynamodb_table" "aviationapi-terraform-lock" {
  name = "aviationapi-terraform-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}

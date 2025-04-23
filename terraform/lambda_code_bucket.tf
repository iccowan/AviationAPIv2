resource "aws_s3_bucket" "aviationapi-source-code" {
  bucket = "aviationapi-source-code${var.ENV_SUFFIX}"
}

resource "aws_s3_bucket_lifecycle_configuration" "aviationapi-source-code-lifecycle" {
  bucket = aws_s3_bucket.aviationapi-source-code.id

  rule {
    id     = "delete-after-30-days"
    status = "Enabled"

    filter {}

    expiration {
      days = 30
    }
  }
}

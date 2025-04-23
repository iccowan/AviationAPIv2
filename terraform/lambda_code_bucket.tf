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

resource "aws_iam_group" "aviationapi-source-code-access-group" {
  name = "BuildS3BucketAccess"
}

resource "aws_iam_policy" "aviationapi-source-code-policy" {
  name = "aviationapi-source-code-role-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "S3GetPutObject"
        Effect   = "Allow"
        Action   = [
          "s3:GetObject",
          "s3:PutObject"
        ],
        Resource = "${aws_s3_bucket.aviationapi-source-code.arn}/*"
      }
    ]
  })
}

resource "aws_iam_group_policy_attachment" "aviationapi-source-code-role-group" {
  group = aws_iam_group.aviationapi-source-code-access-group.name
  policy_arn = aws_iam_policy.aviationapi-source-code-policy.arn
}

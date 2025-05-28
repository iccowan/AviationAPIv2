resource "aws_iam_role" "gha-build-role" {
  name = "GHABuildAssumeRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Federated = aws_iam_openid_connect_provider.gha.arn
        },
        Action = "sts:AssumeRoleWithWebIdentity",
        Condition = {
          StringEquals = {
            "token.actions.githubusercontent.com:aud" = "sts.amazonaws.com"
          },
          StringLike = {
            "token.actions.githubusercontent.com:sub" = "repo:iccowan/AviationAPIv2:*"
          }
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "gha-build-role-s3-bucket-policy" {
  role       = aws_iam_role.gha-build-role.name
  policy_arn = var.CODE_BUCKET_S3_ARN
}

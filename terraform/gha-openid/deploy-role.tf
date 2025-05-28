resource "aws_iam_role" "gha-deploy-role" {
  name = "GHADeployAssumeRole"

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

resource "aws_iam_policy" "aviationapi-deploy-policy" {
  name = "aviationapi-deploy-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "LambdaUpdateCode"
        Effect = "Allow"
        Action = [
          "lambda:UpdateFunctionCode"
        ],
        Resource = var.LAMBDA_FUNCTION_ARNS
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "gha-deploy-role-deploy-policy" {
  role       = aws_iam_role.gha-deploy-role.name
  policy_arn = aws_iam_policy.aviationapi-deploy-policy.arn
}

resource "aws_iam_role_policy_attachment" "gha-deploy-role-s3-bucket-policy" {
  role       = aws_iam_role.gha-deploy-role.name
  policy_arn = var.CODE_BUCKET_S3_ARN
}

resource "aws_iam_role" "gha-terraform-role" {
  name = "GHATerraformAssumeRole"

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

resource "aws_iam_policy" "aviationapi-terraform-policy" {
  name = "aviationapi-terraform-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "*"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "gha-terraform-role-terraform-policy" {
  role       = aws_iam_role.gha-terraform-role.name
  policy_arn = aws_iam_policy.aviationapi-terraform-policy.arn
}


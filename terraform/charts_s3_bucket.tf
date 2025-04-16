resource "aws_s3_bucket" "aviationapi-charts" {
  bucket = "aviationapi${var.ENV_SUFFIX}"
}

resource "aws_s3_bucket_lifecycle_configuration" "aviationapi-charts-lifecycle" {
  bucket = aws_s3_bucket.aviationapi-charts.id

  rule {
    id     = "delete-after-90-days"
    status = "Enabled"

    filter {}

    expiration {
      days = 90
    }
  }
}

resource "aws_s3_bucket_accelerate_configuration" "aviationapi-charts-accelerate" {
  bucket = aws_s3_bucket.aviationapi-charts.id
  status = "Enabled"
}

resource "aws_s3_bucket_public_access_block" "aviationapi-charts-public-access" {
  bucket = aws_s3_bucket.aviationapi-charts.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "aviationapi-charts-policy" {
  bucket = aws_s3_bucket.aviationapi-charts.id

  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "AllowGetObjects"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.aviationapi-charts.arn}/**"
      }
    ]
  })

  depends_on = [
    aws_s3_bucket_public_access_block.aviationapi-charts-public-access
  ]
}

resource "aws_acm_certificate" "aviationapi-charts-cert" {
  domain_name       = "charts${var.ENV_SUFFIX}.${var.DOMAIN}"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

locals {
  s3_origin_id = "${aws_s3_bucket.aviationapi-charts.bucket}-origin"
}

resource "aws_cloudfront_distribution" "aviationapi-charts-cloudfront" {
  origin {
    domain_name = aws_s3_bucket.aviationapi-charts.bucket_regional_domain_name
    origin_id   = local.s3_origin_id
  }

  enabled         = true
  is_ipv6_enabled = true

  aliases = [
    "charts${var.ENV_SUFFIX}.${var.DOMAIN}"
  ]

  default_cache_behavior {
    allowed_methods  = ["HEAD", "GET", "OPTIONS"]
    cached_methods   = ["HEAD", "GET", "OPTIONS"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn = aws_acm_certificate.aviationapi-charts-cert.arn
    ssl_support_method  = "sni-only"
  }
}

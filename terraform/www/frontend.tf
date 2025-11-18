resource "aws_s3_bucket" "aviationapi-www" {
  bucket = "aviationapi-www${var.ENV_SUFFIX}"
}

resource "aws_s3_bucket_public_access_block" "aviationapi-www-public-access" {
  bucket = aws_s3_bucket.aviationapi-www.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_acm_certificate" "aviationapi-www-cert" {
  domain_name       = "www${var.WWW_ENV_SUFFIX}.${var.DOMAIN}"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

locals {
  s3_origin_id = "${aws_s3_bucket.aviationapi-www.bucket}-origin"
}

resource "aws_cloudfront_origin_access_control" "aviationapi-www-cloudfront-oac" {
  name                              = "aviationapi-www-cloudfront-oac"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

resource "aws_cloudfront_distribution" "aviationapi-www-cloudfront" {
  origin {
    domain_name              = aws_s3_bucket.aviationapi-www.bucket_regional_domain_name
    origin_access_control_id = aws_cloudfront_origin_access_control.aviationapi-www-cloudfront-oac.id
    origin_id                = local.s3_origin_id
  }

  enabled             = true
  is_ipv6_enabled     = true
  default_root_object = "index.html"

  aliases = [
    "www${var.WWW_ENV_SUFFIX}.${var.DOMAIN}"
  ]

  default_cache_behavior {
    allowed_methods  = ["HEAD", "GET", "OPTIONS"]
    cached_methods   = ["HEAD", "GET", "OPTIONS"]
    target_origin_id = local.s3_origin_id

    forwarded_values {
      query_string = true

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
    acm_certificate_arn = aws_acm_certificate.aviationapi-www-cert.arn
    ssl_support_method  = "sni-only"
  }

  custom_error_response {
    error_code         = 404
    response_code      = 200
    response_page_path = "/index.html"
  }

  custom_error_response {
    error_code         = 403
    response_code      = 200
    response_page_path = "/index.html"
  }
}

resource "aws_s3_bucket_policy" "aviationapi-www-policy" {
  bucket = aws_s3_bucket.aviationapi-www.id

  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "AllowGetObjects"
    Statement = [
      {
        Sid    = "AllowCloudFrontServicePrincipalReadOnly"
        Effect = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action   = "s3:GetObject"
        Resource = "${aws_s3_bucket.aviationapi-www.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = "${aws_cloudfront_distribution.aviationapi-www-cloudfront.arn}"
          }
        }
      }
    ]
  })
}

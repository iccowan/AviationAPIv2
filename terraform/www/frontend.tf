resource "aws_s3_bucket" "aviationapi-www" {
  bucket = "aviationapi-www${var.ENV_SUFFIX}"
}

resource "aws_s3_bucket_website_configuration" "aviationapi-www" {
  bucket = aws_s3_bucket.aviationapi-www.id

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "index.html"
  }
}

resource "aws_s3_bucket_public_access_block" "aviationapi-www-public-access" {
  bucket = aws_s3_bucket.aviationapi-www.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "aviationapi-www-policy" {
  bucket = aws_s3_bucket.aviationapi-www.id

  policy = jsonencode({
    Version = "2012-10-17"
    Id      = "AllowGetObjects"
    Statement = [
      {
        Sid       = "PublicReadGetObject"
        Effect    = "Allow"
        Principal = "*"
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.aviationapi-www.arn}/**"
      }
    ]
  })

  depends_on = [
    aws_s3_bucket_public_access_block.aviationapi-www-public-access
  ]
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

resource "aws_cloudfront_distribution" "aviationapi-www-cloudfront" {
  origin {
    domain_name = aws_s3_bucket_website_configuration.aviationapi-www.website_endpoint
    origin_id   = local.s3_origin_id
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "http-only"
      origin_ssl_protocols   = ["TLSv1"]
    }
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
    acm_certificate_arn = aws_acm_certificate.aviationapi-www-cert.arn
    ssl_support_method  = "sni-only"
  }

  custom_error_response {
    error_code         = 404
    response_code      = 200
    response_page_path = "/index.html"
  }
}

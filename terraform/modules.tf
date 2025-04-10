module "api" {
  source = "./api"

  ENV              = var.ENV
  SUBDOMAIN_APPEND = var.SUBDOMAIN_APPEND
}

module "db" {
  source = "./db"
}

module "chart-processing" {
  source = "./chart-processing"

  S3_BUCKET = aws_s3_bucket.aviationapi-charts
}

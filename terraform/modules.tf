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
  AIRPORTS_TABLE_ARN = module.db.aviationapi-airports-table-arn
  AIRAC_TABLE_ARN = module.db.aviationapi-airac-table-arn
  CHARTS_BASE_URL = "https://${aws_cloudfront_distribution.aviationapi-charts.aliases[0]}"
}

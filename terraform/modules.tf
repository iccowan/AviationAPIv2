module "api" {
  source = "./api"

  DOMAIN     = var.DOMAIN
  ENV        = var.ENV
  ENV_SUFFIX = var.ENV_SUFFIX
}

module "db" {
  source = "./db"
}

module "chart-processing" {
  source = "./chart-processing"

  S3_BUCKET          = aws_s3_bucket.aviationapi-charts
  AIRPORTS_TABLE = module.db.aviationapi-airports-table
  CHARTS_BASE_URL    = "https://${tolist(aws_cloudfront_distribution.aviationapi-charts.aliases)[0]}"
}

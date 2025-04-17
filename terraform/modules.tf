module "api" {
  source = "./api"

  DOMAIN     = var.DOMAIN
  ENV        = var.ENV
  ENV_SUFFIX = var.ENV_SUFFIX
}

module "db" {
  source = "./db"
}

module "chart-pre-processing" {
  source = "./chart-pre-processing"

  TRIGGER_CHART_PROCESSOR_TOPIC = module.chart-processing.trigger-chart-processor-topic
  AIRAC_TABLE = module.db.aviationapi-airac-table
}

module "chart-processing" {
  source = "./chart-processing"

  S3_BUCKET       = aws_s3_bucket.aviationapi-charts
  AIRPORTS_TABLE  = module.db.aviationapi-airports-table
  CHARTS_BASE_URL = "https://${tolist(aws_cloudfront_distribution.aviationapi-charts-cloudfront.aliases)[0]}"
  TRIGGER_CHART_POST_PROCESSOR_TOPIC = module.chart-post-processing.trigger-chart-post-processor-topic
}

module "chart-post-processing" {
  source = "./chart-post-processing"
}

module "db" {
  source = "./db"
}

module "api" {
  source = "./api"

  DOMAIN         = var.DOMAIN
  ENV            = var.ENV
  ENV_SUFFIX     = var.ENV_SUFFIX
  AIRAC_TABLE    = module.db.aviationapi-airac-table
  AIRPORTS_TABLE = module.db.aviationapi-airports-table
  INIT_LAMBDA    = var.INIT_LAMBDA
}

module "chart-pre-processing" {
  source = "./chart-pre-processing"

  TRIGGER_CHART_PROCESSOR_TOPIC = module.chart-processing.trigger-chart-processor-topic
  AIRAC_TABLE                   = module.db.aviationapi-airac-table
  INIT_LAMBDA                   = var.INIT_LAMBDA
}

module "chart-processing" {
  source = "./chart-processing"

  S3_BUCKET                          = aws_s3_bucket.aviationapi-charts
  AIRPORTS_TABLE                     = module.db.aviationapi-airports-table
  CHARTS_BASE_URL                    = "https://${tolist(aws_cloudfront_distribution.aviationapi-charts-cloudfront.aliases)[0]}"
  TRIGGER_CHART_POST_PROCESSOR_TOPIC = module.chart-post-processing.trigger-chart-post-processor-topic
  INIT_LAMBDA                        = var.INIT_LAMBDA
}

module "chart-post-processing" {
  source = "./chart-post-processing"

  AIRAC_TABLE                       = module.db.aviationapi-airac-table
  AIRAC_CYCLE_CHART_TYPE_INDEX_NAME = module.db.aviationapi-airac-table-airac-cycle-chart-type-index-name
  INIT_LAMBDA                       = var.INIT_LAMBDA
}

module "gha-openid" {
  source = "./gha-openid"

  LAMBDA_FUNCTION_ARNS = [
    module.api.lambda-function.arn,
    module.chart-pre-processing.lambda-function.arn,
    module.chart-processing.lambda-function.arn,
    module.chart-post-processing.lambda-function.arn
  ]
  CODE_BUCKET_S3_ARN = aws_iam_policy.aviationapi-source-code-policy.arn
}

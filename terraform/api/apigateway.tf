resource "aws_api_gateway_rest_api" "aviationapi" {
  name        = "aviation-api"
  description = "Main AviationAPI API"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "root" {
  rest_api_id = aws_api_gateway_rest_api.aviationapi.id
  parent_id   = aws_api_gateway_rest_api.aviationapi.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy" {
  rest_api_id   = aws_api_gateway_rest_api.aviationapi.id
  resource_id   = aws_api_gateway_resource.root.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = aws_api_gateway_rest_api.aviationapi.id
  resource_id             = aws_api_gateway_resource.root.id
  http_method             = aws_api_gateway_method.proxy.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.aviationapi_lambda.invoke_arn
}

resource "aws_api_gateway_deployment" "deployment" {
  depends_on = [
    aws_api_gateway_integration.lambda_integration
    ]
  
  rest_api_id = aws_api_gateway_rest_api.aviationapi.id
  }

resource "aws_api_gateway_stage" "deployment" {
  deployment_id = aws_api_gateway_deployment.deployment.id
  rest_api_id   = aws_api_gateway_rest_api.aviationapi.id
  stage_name    = var.ENV
  }

resource "aws_acm_certificate" "aviationapi" {
  domain_name = "api${var.SUBDOMAIN_APPEND}.aviationapi.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate_validation" "aviationapi" {
  certificate_arn = aws_acm_certificate.aviationapi.arn
}

resource "aws_api_gateway_domain_name" "aviationapi" {
  depends_on = [
    aws_acm_certificate_validation.aviationapi
  ]

  certificate_arn = aws_acm_certificate_validation.aviationapi.certificate_arn
  domain_name = "api${var.SUBDOMAIN_APPEND}.aviationapi.com"
}

resource "aws_api_gateway_base_path_mapping" "aviationapi" {
  api_id = aws_api_gateway_rest_api.aviationapi.id
  stage_name = aws_api_gateway_stage.deployment.stage_name
  domain_name = aws_api_gateway_domain_name.aviationapi.domain_name
  base_path = "v2"
}


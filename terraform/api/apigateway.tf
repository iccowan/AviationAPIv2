resource "aws_api_gateway_rest_api" "aviationapi-api-apigateway" {
  name = "aviation-api"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "aviationapi-api-root" {
  rest_api_id = aws_api_gateway_rest_api.aviationapi-api-apigateway.id
  parent_id   = aws_api_gateway_rest_api.aviationapi-api-apigateway.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "aviationapi-api-proxy" {
  rest_api_id   = aws_api_gateway_rest_api.aviationapi-api-apigateway.id
  resource_id   = aws_api_gateway_resource.aviationapi-api-root.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "aviationapi-api-lambda-integration" {
  rest_api_id             = aws_api_gateway_rest_api.aviationapi-api-apigateway.id
  resource_id             = aws_api_gateway_resource.aviationapi-api-root.id
  http_method             = aws_api_gateway_method.aviationapi-api-proxy.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.aviationapi-api-lambda.invoke_arn
}

resource "aws_api_gateway_deployment" "aviationapi-api-deployment" {
  depends_on = [
    aws_api_gateway_integration.aviationapi-api-lambda-integration
  ]

  rest_api_id = aws_api_gateway_rest_api.aviationapi-api-apigateway.id
}

resource "aws_api_gateway_stage" "aviationapi-api-stage" {
  deployment_id = aws_api_gateway_deployment.aviationapi-api-deployment.id
  rest_api_id   = aws_api_gateway_rest_api.aviationapi-api-apigateway.id
  stage_name    = var.ENV
}

resource "aws_acm_certificate" "aviationapi-api-cert" {
  domain_name       = "api${var.ENV_SUFFIX}.${var.DOMAIN}"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate_validation" "aviationapi-api-cert" {
  certificate_arn = aws_acm_certificate.aviationapi-api-cert.arn
}

resource "aws_api_gateway_domain_name" "aviationapi-api-apigateway-domain" {
  certificate_arn = aws_acm_certificate_validation.aviationapi-api-cert.certificate_arn
  domain_name     = "api${var.ENV_SUFFIX}.${var.DOMAIN}"

  depends_on = [
    aws_acm_certificate_validation.aviationapi-api-cert
  ]
}

resource "aws_api_gateway_base_path_mapping" "aviationapi-api-uri-mapping" {
  api_id      = aws_api_gateway_rest_api.aviationapi-api-apigateway.id
  stage_name  = aws_api_gateway_stage.aviationapi-api-stage.stage_name
  domain_name = aws_api_gateway_domain_name.aviationapi-api-apigateway-domain.domain_name
  base_path   = "v2"
}


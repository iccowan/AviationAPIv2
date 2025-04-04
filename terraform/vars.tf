variable "AWS_REGION" {
  default = "us-east-1"
}

variable "PY_VERSION" {
  default = "python3.12"
}

variable "S3_BUCKET" {
  default = "deployment-images"
}

variable "S3_KEY" {
  default = "api/deploy-1.zip"
}

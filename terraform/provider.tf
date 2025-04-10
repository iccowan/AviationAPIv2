terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.94.0"
    }
  }
}

provider "aws" {
  region = var.AWS_REGION

  endpoints {
    dynamodb = var.DYNAMODB_ENDPOINT
  }
}

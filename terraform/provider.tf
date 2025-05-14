terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.94.0"
    }
  }

  backend "s3" {
    bucket = "aviationapi-terraform-state"
    profile = "aviationapi-terraform"
    key = "terraform.tfstate"
    region = "us-east-1"
    dynamodb_table = "aviationapi-terraform-lock"
    encrypt = true
  }
}

provider "aws" {
  region = var.AWS_REGION

  endpoints {
    dynamodb = var.DYNAMODB_ENDPOINT
  }
}

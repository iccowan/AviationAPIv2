variable "AWS_REGION" {
  default = "us-east-1"
}

variable "DOMAIN" {
  default = "aviationapi.com"
}

variable "ENV" {
  default = "sandbox"
}

variable "SUBDOMAIN_APPEND" {
  default = "-sandbox"
}

variable "DYNAMODB_ENDPOINT" {
  default = ""
}

variable "PY_VERSION" {
  default = "python3.13"
}

variable "SOURCE_DIR" {
  default = "../chart-processor/build"
}

variable "OUTPUT_PATH" {
  default = "../chart-processor/build.zip"
}

variable "S3_BUCKET" {}
variable "AIRPORTS_TABLE_ARN" {}
variable "AIRAC_TABLE_ARN" {}

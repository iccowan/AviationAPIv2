variable "PY_VERSION" {
  default = "python3.13"
}

variable "SOURCE_DIR" {
  default = "../src/chart-processor/build"
}

variable "OUTPUT_PATH" {
  default = "../src/chart-processor/build.zip"
}

variable "S3_BUCKET" {}
variable "AIRPORTS_TABLE" {}
variable "CHARTS_BASE_URL" {}

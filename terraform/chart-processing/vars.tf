variable "PY_VERSION" {
  default = "python3.13"
}

variable "SOURCE_DIR" {
  default = "../src/aviationapi/chart_processor/build"
}

variable "OUTPUT_PATH" {
  default = "../src/aviationapi/chart_processor/build.zip"
}

variable "S3_BUCKET" {}
variable "AIRPORTS_TABLE" {}
variable "CHARTS_BASE_URL" {}
variable "TRIGGER_CHART_POST_PROCESSOR_TOPIC" {}

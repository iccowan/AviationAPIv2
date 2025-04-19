variable "PY_VERSION" {
  default = "python3.13"
}

variable "SOURCE_DIR" {
  default = "../src/aviationapi/chart_post_processor/build"
}

variable "OUTPUT_PATH" {
  default = "../src/aviationapi/chart_post_processor/build.zip"
}

variable "AIRAC_TABLE" {}
variable "AIRAC_CYCLE_CHART_TYPE_INDEX_NAME" {}

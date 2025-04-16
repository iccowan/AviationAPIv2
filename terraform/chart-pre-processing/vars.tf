variable "PY_VERSION" {
  default = "python3.13"
}

variable "SOURCE_DIR" {
  default = "../src/aviationapi/chart_pre_processor/build"
}

variable "OUTPUT_PATH" {
  default = "../src/aviationapi/chart_pre_processor/build.zip"
}

variable "TRIGGER_CHART_PROCESSOR_TOPIC" {}
variable "AIRAC_TABLE" {}

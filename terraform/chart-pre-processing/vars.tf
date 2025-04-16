variable "PY_VERSION" {
  default = "python3.13"
}

variable "SOURCE_DIR" {
  default = "../src/chart-pre-processor/build"
}

variable "OUTPUT_PATH" {
  default = "../src/chart-pre-processor/build.zip"
}

variable "TRIGGER_CHART_PROCESSOR_TOPIC" {}
variable "AIRAC_TABLE" {}

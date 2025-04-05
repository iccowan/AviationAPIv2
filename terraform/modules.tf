module "api" {
  source = "./api"
  
  ENV = var.ENV
  SUBDOMAIN_APPEND = var.SUBDOMAIN_APPEND
}

terraform {
  backend "azurerm" {
    resource_group_name   = "tfstate2-rg"
    storage_account_name  = "vithutfstateacct"
    container_name        = "tfstate"
    key                   = "autoheal2.terraform.tfstate"
  }
}

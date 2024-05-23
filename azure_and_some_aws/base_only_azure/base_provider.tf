terraform {
<<<<<<< HEAD
    required_version = ">=1.8.0"
    required_providers {
        azurerm = {
            source  = "hashicorp/azurerm"
            version = "~> 3.103.0"
=======
    required_version = ">=1.0.0"
    required_providers {
        azurerm = {
            source  = "hashicorp/azurerm"
            version = "~> 3.98.0"
>>>>>>> b66ab7998d37aebe3d3ca438b5ec6b669aa9f44c
        }
    }
}

provider "azurerm" {
    features {}
}
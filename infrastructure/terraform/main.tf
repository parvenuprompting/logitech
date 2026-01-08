terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0"
    }
  }
}

provider "azurerm" {
  features {}
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "westeurope"
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
  default     = "logitech-fleet"
}

variable "environment" {
  description = "Environment (dev, poc, prod)"
  type        = string
  default     = "dev"
}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
  tags = {
    Project     = "LogiTech Fleet"
    Environment = var.environment
  }
}

module "event_hubs" {
  source              = "./modules/event_hubs"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  namespace_name      = "eh-${var.project_name}-${var.environment}"
}

module "data_lake" {
  source              = "./modules/data_lake"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  storage_account_name = replace("sa${var.project_name}${var.environment}", "-", "")
}

module "databricks" {
  source              = "./modules/databricks"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  workspace_name      = "dbw-${var.project_name}-${var.environment}"
}

output "event_hub_namespace_name" {
  value = module.event_hubs.eventhub_namespace_id
}

output "data_lake_account_name" {
  value = module.data_lake.storage_account_name
}

output "databricks_workspace_url" {
  value = module.databricks.workspace_url
}

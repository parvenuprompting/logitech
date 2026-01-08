variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "storage_account_name" { type = string }

resource "azurerm_storage_account" "datalake" {
  name                     = var.storage_account_name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS" # Change to GRS for Prod
  account_kind             = "StorageV2"
  is_hns_enabled           = true   # Hierarchical Namespace required for Data Lake Gen2

  tags = {
    Environment = "Dev" # Should be dynamic
  }
}

resource "azurerm_storage_data_lake_gen2_filesystem" "bronze" {
  name               = "bronze"
  storage_account_id = azurerm_storage_account.datalake.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "silver" {
  name               = "silver"
  storage_account_id = azurerm_storage_account.datalake.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "gold" {
  name               = "gold"
  storage_account_id = azurerm_storage_account.datalake.id
}

resource "azurerm_storage_data_lake_gen2_filesystem" "checkpoint" {
  name               = "checkpoints"
  storage_account_id = azurerm_storage_account.datalake.id
}

# Lifecycle Management Policy
resource "azurerm_storage_management_policy" "retention_policy" {
  storage_account_id = azurerm_storage_account.datalake.id

  rule {
    name    = "delete-audit-files-after-7-years"
    enabled = true
    filters {
      prefix_match = ["bronze/audit/"]
      blob_types   = ["blockBlob"]
    }
    actions {
      base_blob {
        delete_after_days_since_modification_greater_than = 2555 # 7 years
      }
    }
  }
}

output "storage_account_name" {
  value = azurerm_storage_account.datalake.name
}

output "storage_account_id" {
  value = azurerm_storage_account.datalake.id
}

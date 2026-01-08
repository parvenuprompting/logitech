variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "details" {
  type = object({
    name = string
  })
}

resource "azurerm_cosmosdb_account" "db" {
  name                = var.details.name
  location            = var.location
  resource_group_name = var.resource_group_name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = var.location
    failover_priority = 0
  }

  capabilities {
    name = "EnableServerless"
  }
}

resource "azurerm_cosmosdb_sql_database" "fleet" {
  name                = "fleet_db"
  resource_group_name = var.resource_group_name
  account_name        = azurerm_cosmosdb_account.db.name
}

resource "azurerm_cosmosdb_sql_container" "alerts" {
  name                = "active_alerts"
  resource_group_name = var.resource_group_name
  account_name        = azurerm_cosmosdb_account.db.name
  database_name       = azurerm_cosmosdb_sql_database.fleet.name
  partition_key_path  = "/vehicle_id"
  default_ttl         = 86400 # 24 uur retention (ephemeral)
}

output "endpoint" {
  value = azurerm_cosmosdb_account.db.endpoint
}

output "primary_key" {
  value     = azurerm_cosmosdb_account.db.primary_key
  sensitive = true
}

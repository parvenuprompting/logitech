variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "workspace_name" { type = string }

resource "azurerm_databricks_workspace" "workspace" {
  name                = var.workspace_name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = "premium" # Required for some advanced features like Unity Catalog capability assurance

  tags = {
    Environment = "Dev"
  }
}

output "workspace_url" {
  value = azurerm_databricks_workspace.workspace.workspace_url
}

output "workspace_id" {
  value = azurerm_databricks_workspace.workspace.id
}

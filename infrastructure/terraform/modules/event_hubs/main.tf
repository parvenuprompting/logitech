variable "location" {
  description = "Azure region"
  type        = string
  default     = "westeurope"
}

variable "resource_group_name" {
  description = "Resource Group Name"
  type        = string
}

variable "namespace_name" {
  description = "Event Hub Namespace Name"
  type        = string
}

variable "schema_registry_group_name" {
    description = "Name for the Schema Registry Group"
    type = string
    default = "fleet-telemetry-schemas"
}

resource "azurerm_eventhub_namespace" "eh_ns" {
  name                = var.namespace_name
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "Standard"
  capacity            = 1

  tags = {
    Environment = "Production"
    Project     = "LogiTech Fleet"
  }
}

resource "azurerm_eventhub_namespace_schema_group" "schema_group" {
  name                 = var.schema_registry_group_name
  namespace_id         = azurerm_eventhub_namespace.eh_ns.id
  schema_compatibility = "Backward"
  schema_type          = "Avro" # Azure Schema Registry supports Avro primarily currently, but JSON support is growing. We stick to infra definition.
}

output "eventhub_namespace_id" {
  value = azurerm_eventhub_namespace.eh_ns.id
}

output "schema_group_id" {
  value = azurerm_eventhub_namespace_schema_group.schema_group.id
}

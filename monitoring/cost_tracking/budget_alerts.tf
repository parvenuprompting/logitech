
resource "azurerm_consumption_budget_resource_group" "dev_budget" {
  name              = "dev-budget-monthly"
  resource_group_id = var.resource_group_id
  amount            = 2000
  time_grain        = "Monthly"

  time_period {
    start_date = "2026-01-01T00:00:00Z"
  }

  notification {
    enabled   = true
    threshold = 80.0
    operator  = "EqualTo"

    contact_emails = [
      "admin@logitech.com",
      "data-platform@logitech.com"
    ]
  }

  notification {
    enabled   = true
    threshold = 100.0
    operator  = "EqualTo"
    
    # In a real scenario, you might trigger an Action Group here to disable resources
    contact_emails = [
      "admin@logitech.com",
      "head-of-engineering@logitech.com"
    ]
  }
}

# Action Group for Slack Notification (Conceptual)
resource "azurerm_monitor_action_group" "slack_alert" {
  name                = "slack-cost-alert"
  resource_group_name = var.resource_group_name
  short_name          = "CostAlert"

  email_receiver {
    name          = "slack-email-integration"
    email_address = "alerts-channel@logitech.slack.com"
  }
}

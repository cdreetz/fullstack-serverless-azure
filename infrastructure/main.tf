# configure azure provider
provider "azurerm" {
  subscription_id = "2ffdad1a-8515-4dfd-b10f-ade0a848124a"
  features {}
}

# create resource group
resource "azurerm_resource_group" "rg" {
  name     = "my-static-app_group"
  location = "West US 2"
}

# reference existing static web app
resource "azurerm_static_site" "web" {
  name                = "my-static-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
}

# storage account
resource "azurerm_storage_account" "sa" {
  name                     = "mystorageaccount6969420"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "asp" {
  name                = "WestUS2LinuxDynamicPlan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

# func app
resource "azurerm_linux_function_app" "func" {
  name                = "my-fastapi-function"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  storage_account_name       = azurerm_storage_account.sa.name
  storage_account_access_key = azurerm_storage_account.sa.primary_access_key
  service_plan_id            = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      python_version = "3.11"
    }
  }
}


# output the default hostname of the static web app
output "static_web_app_url" {
  value = azurerm_static_site.web.default_host_name
}

# output the api key for deploying to the static web app
output "static_web_app_api_key" {
  value     = azurerm_static_site.web.api_key
  sensitive = true
}

output "function_app_url" {
  value = azurerm_linux_function_app.func.default_hostname
}

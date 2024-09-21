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

# output the default hostname of the static web app
output "static_web_app_url" {
  value = azurerm_static_site.web.default_host_name
}

# output the api key for deploying to the static web app
output "static_web_app_api_key" {
  value     = azurerm_static_site.web.api_key
  sensitive = true
}

# Configure Azure provider
provider "azurerm" {
  subscription_id = "2ffdad1a-8515-4dfd-b10f-ade0a848124a"
  features {}
}

# Configure Azure AD provider
provider "azuread" {}

# Create new resource group
resource "azurerm_resource_group" "rg" {
  name     = "my-secured-app-rg"
  location = "West US 2"
}

# Create VNet
resource "azurerm_virtual_network" "vnet" {
  name                = "my-secure-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

# Create subnets
resource "azurerm_subnet" "static_web_subnet" {
  name                 = "static-web-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.1.0/24"]
}

resource "azurerm_subnet" "function_subnet" {
  name                 = "function-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/24"]

  delegation {
    name = "serverFarms"
    service_delegation {
      name    = "Microsoft.Web/serverFarms"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

resource "azurerm_subnet" "storage_subnet" {
  name                 = "storage-subnet"
  resource_group_name  = azurerm_resource_group.rg.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.3.0/24"]
  service_endpoints    = ["Microsoft.Storage"]
}

# Create Static Web App
resource "azurerm_static_web_app" "web" {
  name                = "my-new-static-app"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
}

# Create private endpoint for static web app
resource "azurerm_private_endpoint" "static_web_endpoint" {
  name                = "static-web-endpoint"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.static_web_subnet.id

  private_service_connection {
    name                           = "static-web-connection"
    private_connection_resource_id = azurerm_static_web_app.web.id
    is_manual_connection           = false
    subresource_names              = ["staticSites"]
  }
}

# Random string for unique storage account name
resource "random_string" "random" {
  length  = 8
  special = false
  upper   = false
}

# Create Storage account
resource "azurerm_storage_account" "sa" {
  name                     = "mynewstorageacc${random_string.random.result}"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  network_rules {
    default_action = "Deny"
    virtual_network_subnet_ids = [azurerm_subnet.storage_subnet.id]
  }
}

# Create private endpoint for storage account
resource "azurerm_private_endpoint" "storage_endpoint" {
  name                = "storage-endpoint"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.storage_subnet.id

  private_service_connection {
    name                           = "storage-connection"
    private_connection_resource_id = azurerm_storage_account.sa.id
    is_manual_connection           = false
    subresource_names              = ["blob"]
  }
}

# Create App Service Plan
resource "azurerm_service_plan" "asp" {
  name                = "new-west-us-2-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1"
}

# Get current Azure client configuration
data "azurerm_client_config" "current" {}

# Create Azure AD Application
resource "azuread_application" "app" {
  display_name = "My Secured App"
  web {
    homepage_url  = "https://${azurerm_static_web_app.web.default_host_name}"
    redirect_uris = ["https://${azurerm_static_web_app.web.default_host_name}/.auth/login/aad/callback"]
  }
}

# Create App Registration
resource "azuread_service_principal" "sp" {
  client_id = azuread_application.app.client_id
}

# Create Function App
resource "azurerm_linux_function_app" "func" {
  name                       = "my-new-fastapi-function"
  resource_group_name        = azurerm_resource_group.rg.name
  location                   = azurerm_resource_group.rg.location
  storage_account_name       = azurerm_storage_account.sa.name
  storage_account_access_key = azurerm_storage_account.sa.primary_access_key
  service_plan_id            = azurerm_service_plan.asp.id

  site_config {
    application_stack {
      python_version = "3.11"
    }
    vnet_route_all_enabled = true
  }

  virtual_network_subnet_id = azurerm_subnet.function_subnet.id

  auth_settings {
    enabled                       = true
    issuer                        = "https://sts.windows.net/${data.azurerm_client_config.current.tenant_id}/"
    unauthenticated_client_action = "RedirectToLoginPage"
    default_provider              = "AzureActiveDirectory"
    active_directory {
      client_id = azuread_application.app.client_id
    }
  }
}

# Create private endpoint for function app
resource "azurerm_private_endpoint" "function_endpoint" {
  name                = "function-endpoint"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  subnet_id           = azurerm_subnet.function_subnet.id

  private_service_connection {
    name                           = "function-connection"
    private_connection_resource_id = azurerm_linux_function_app.func.id
    is_manual_connection           = false
    subresource_names              = ["sites"]
  }
}

# Outputs
output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "static_web_app_name" {
  value = azurerm_static_web_app.web.name
}

output "static_web_app_url" {
  value = azurerm_static_web_app.web.default_host_name
}

output "function_app_name" {
  value = azurerm_linux_function_app.func.name
}

output "function_app_url" {
  value = azurerm_linux_function_app.func.default_hostname
}

output "storage_account_name" {
  value = azurerm_storage_account.sa.name
}

output "vnet_name" {
  value = azurerm_virtual_network.vnet.name
}

output "app_registration_id" {
  value = azuread_application.app.client_id
}

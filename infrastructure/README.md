# Infrastructure

This directory contains all the Infrastructure as Code (IaC) templates needed to set up the Azure resources for our project.

## Structure

- `/modules/`: Reusable Terraform modules
- `/environments/`: Environment-specific configurations

## Prerequisites

- Terraform v1.0+
- Azure CLI
- Azure subscription

## Setup

1. Install Terraform and Azure CLI
2. Login to Azure: `az login`
3. Select your subscription: `az account set --subscription <subscription_id>`

## Usage

1. Navigate to the environment directory you want to deploy (e.g., `/environments/dev`)
2. Initialize Terraform: `terraform init`
3. Plan the deployment: `terraform plan -out=tfplan`
4. Apply the changes: `terraform apply tfplan`

## Available Resources

- Virtual Network
- Azure Functions
- Azure Static Web Apps
- Azure API Management
- Azure Active Directory configurations
- Network Security Groups

## Best Practices

- Use remote state storage in Azure Storage Account
- Use Terraform workspaces for different environments
- Keep secrets in Azure Key Vault and reference them in Terraform

## Troubleshooting

If you encounter issues, check the Azure portal for resource status and review Terraform logs.

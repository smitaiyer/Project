# Azure Storage API Reference

## Overview

Azure Storage provides a massively scalable cloud storage solution for data objects. This API reference documents all endpoints, methods, and parameters. For an introduction to Azure storage, see the getting started guide.

## Authentication

All requests must include an authentication token. The token can be obtained by using the Azure SDK. It's recommended that you store your credentials securely.

### Obtaining a Token

Here's how to get a token:

1. Create a service principal in azure AD
2. Assign the appropriate roles to it
3. Use the SDK to authenticate

The token is returned by the service and can be used in subsequent requests.

## Endpoints

### Create Storage Account

**Endpoint**: `POST /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts`

**Parameters**:

- `subscriptionId` (string): The subscription identifier. This is required.
- `resourceGroupName` (string): The name of the resource group. It's important that this is created first.
- `location` (string): The geographic location for the storage account, such as eastus or westeurope
- `sku` (object): The pricing tier (Standard_LRS, Premium_LRS, etc.)

**Request Example**:

```json
{
  "location": "eastus",
  "sku": {
    "name": "Standard_LRS"
  },
  "kind": "StorageV2",
  "properties": {
    "minimumTlsVersion": "TLS1_2"
  }
}
```

**Response**: A storage account object is returned if the request is successful. The account is provisioned, and you can start using it right away.

### List Storage Accounts

**Endpoint**: `GET /subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Storage/storageAccounts`

This endpoint retrieves all storage accounts in a resource group.

**Parameters**:

- `subscriptionId` (string): The subscription identifier
- `resourceGroupName` (string): The name of the resource group

**Response**: An array of storage account objects. Each object contains the account properties, access keys, and other metadata.

## Error Codes

The API returns the following error codes:

- `400` – The request is invalid
- `401` – Authentication failed. Make sure that your credentials are correct.
- `403` – Access is denied
- `404` – The resource cannot be found
- `500` – An internal server error has occurred

## Limits and Quotas

Several limits apply to storage accounts:

- Max storage per account: 5 PB
- Max throughput: 20 Gbps (ingress), 25 Gbps (egress)
- Max number of resource groups per subscription: 980

For more information about limits, check the service documentation. It provides detailed information about quotas, see the Azure Storage documentation for comprehensive details.

---

## Deprecations

**Note**: The old authentication method (using connection strings) is deprecated and shouldn't be used. Use managed identities instead. The legacy endpoint `/api/v1/` is no longer supported and will be removed in Q4 2025.

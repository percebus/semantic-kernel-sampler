# Conditional Access Policy Troubleshooting Guide

## Error: "Access has been blocked by Conditional Access policies"

### Immediate Actions:

1. **Check Azure AD Configuration:**
   ```bash
   # Verify your service principal exists and has correct permissions
   az ad app list --display-name "your-app-name"
   az ad sp list --display-name "your-app-name"
   ```

2. **Review Conditional Access Policies:**
   - Azure Portal → Azure AD → Security → Conditional Access
   - Look for policies affecting "All cloud apps" or specific Azure services
   - Check if your service principal is excluded

3. **Test Authentication Locally:**
   ```bash
   # Test with Azure CLI (uses different auth flow)
   az login --service-principal -u CLIENT_ID -p CLIENT_SECRET --tenant TENANT_ID
   az account show
   ```

### Solutions by Environment:

#### **Production (Azure-hosted):**
```csharp
// Use Managed Identity - bypasses most CA policies
services.AddAzureAuthenticationWithCASupport(configuration);
```

#### **Development:**
```csharp
// Use DefaultAzureCredential with specific exclusions
var credential = new DefaultAzureCredential(new DefaultAzureCredentialOptions
{
    TenantId = configuration["AzureAd:TenantId"],
    ExcludeSharedTokenCacheCredential = true, // Often blocked
    ExcludeInteractiveBrowserCredential = true
});
```

#### **Certificate-based (Most CA-friendly):**
```csharp
// Upload certificate to Azure AD app registration first
services.AddCertificateCredential(configuration);
```

### Configuration Updates Needed:

1. **For Managed Identity:**
   ```json
   {
     "AzureAd": {
       "TenantId": "your-tenant-id"
       // ClientId only needed for user-assigned MI
     }
   }
   ```

2. **For Client Secret (with CA workarounds):**
   ```json
   {
     "AzureAd": {
       "TenantId": "your-tenant-id",
       "ClientId": "your-client-id",
       "ClientSecret": "your-client-secret",
       "Instance": "https://login.microsoftonline.com/"
     }
   }
   ```

3. **For Certificate:**
   ```json
   {
     "AzureAd": {
       "TenantId": "your-tenant-id",
       "ClientId": "your-client-id",
       "CertificateThumbprint": "your-cert-thumbprint"
     }
   }
   ```

### Azure Portal Configuration:

1. **Service Principal Permissions:**
   - Go to App registrations → Your app → API permissions
   - Add: `Azure Service Management` → `user_impersonation`
   - Add: `Azure OpenAI` → `Cognitive Services OpenAI User`
   - Grant admin consent

2. **Conditional Access Exclusion:**
   - Go to Azure AD → Security → Conditional Access
   - Edit relevant policies
   - Under "Exclude" → "Users and groups" → Add your service principal

3. **Enable Managed Identity (for Azure-hosted apps):**
   - App Service: Settings → Identity → System assigned → On
   - Container: Add `--assign-identity` flag
   - VM: Add managed identity in Azure portal

### Testing Commands:

```bash
# Test authentication
curl -X POST "https://login.microsoftonline.com/{tenant-id}/oauth2/v2.0/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "client_id={client-id}&client_secret={client-secret}&scope=https://management.azure.com/.default&grant_type=client_credentials"

# Test Azure OpenAI access
curl -X GET "https://{resource}.openai.azure.com/openai/deployments?api-version=2023-05-15" \
  -H "Authorization: Bearer {token}"
```

### Error Codes and Solutions:

- **AADSTS53003**: Blocked by CA policy → Use Managed Identity or exclude service principal
- **AADSTS70011**: Invalid scope → Check API permissions and scope format
- **AADSTS700016**: Application not found → Verify ClientId and TenantId
# Example usage of the Bitwarden Secrets CLI tool in PowerShell

Write-Host "=== Bitwarden Secrets CLI Examples (PowerShell) ===" -ForegroundColor Green
Write-Host

# Example 1: Basic usage with environment variables
Write-Host "1. Basic usage with environment variables:" -ForegroundColor Yellow
Write-Host "   bw-secrets inject --shell powershell | Invoke-Expression"
Write-Host

# Example 2: Specify secrets directly
Write-Host "2. Specify secrets directly:" -ForegroundColor Yellow
Write-Host "   bw-secrets inject --shell powershell --secret-keys 'api-key,database-password' --secret-vars 'API_KEY,DB_PASSWORD' | Invoke-Expression"
Write-Host

# Example 3: Quiet mode
Write-Host "3. Quiet mode (suppress info messages):" -ForegroundColor Yellow
Write-Host "   bw-secrets inject --shell powershell --quiet | Invoke-Expression"
Write-Host

# Example 4: List available secrets
Write-Host "4. List available secrets:" -ForegroundColor Yellow
Write-Host "   bw-secrets list-secrets"
Write-Host

# Example 5: Show configuration
Write-Host "5. Show configuration:" -ForegroundColor Yellow
Write-Host "   bw-secrets config"
Write-Host

# Example 6: Development vs Production
Write-Host "6. Development vs Production environments:" -ForegroundColor Yellow
Write-Host "   # Development"
Write-Host "   bw-secrets inject --shell powershell --secret-keys 'dev-api-key,dev-db-password' --secret-vars 'API_KEY,DB_PASSWORD' | Invoke-Expression"
Write-Host
Write-Host "   # Production"
Write-Host "   bw-secrets inject --shell powershell --secret-keys 'prod-api-key,prod-db-password' --secret-vars 'API_KEY,DB_PASSWORD' | Invoke-Expression"
Write-Host

# Example 7: PowerShell profile integration
Write-Host "7. PowerShell profile integration (add to $PROFILE):" -ForegroundColor Yellow
Write-Host "   function Load-Secrets {"
Write-Host "       bw-secrets inject --shell powershell --quiet | Invoke-Expression"
Write-Host "   }"
Write-Host "   Set-Alias -Name secrets -Value Load-Secrets"
Write-Host

# Example 8: Function with error handling
Write-Host "8. Function with error handling:" -ForegroundColor Yellow
Write-Host "   function Load-Secrets {"
Write-Host "       try {"
Write-Host "           bw-secrets inject --shell powershell --quiet | Invoke-Expression"
Write-Host "           Write-Host 'Secrets loaded successfully' -ForegroundColor Green"
Write-Host "       } catch {"
Write-Host "           Write-Host 'Failed to load secrets' -ForegroundColor Red"
Write-Host "           Write-Host `$_.Exception.Message -ForegroundColor Red"
Write-Host "       }"
Write-Host "   }"
Write-Host

Write-Host "=== End of Examples ===" -ForegroundColor Green 
#!/bin/bash
# Example usage of the Bitwarden Secrets CLI tool

echo "=== Bitwarden Secrets CLI Examples ==="
echo

# Example 1: Basic usage with environment variables
echo "1. Basic usage with environment variables:"
echo "   eval \$(bw-secrets inject)"
echo

# Example 2: Specify secrets directly
echo "2. Specify secrets directly:"
echo "   eval \$(bw-secrets inject \\"
echo "     --secret-keys \"api-key,database-password\" \\"
echo "     --secret-vars \"API_KEY,DB_PASSWORD\")"
echo

# Example 3: PowerShell usage
echo "3. PowerShell usage:"
echo "   bw-secrets inject --shell powershell | Invoke-Expression"
echo

# Example 4: Fish shell usage
echo "4. Fish shell usage:"
echo "   bw-secrets inject --shell fish | source"
echo

# Example 5: Quiet mode
echo "5. Quiet mode (suppress info messages):"
echo "   eval \$(bw-secrets inject --quiet)"
echo

# Example 6: List available secrets
echo "6. List available secrets:"
echo "   bw-secrets list-secrets"
echo

# Example 7: Show configuration
echo "7. Show configuration:"
echo "   bw-secrets config"
echo

# Example 8: Development vs Production
echo "8. Development vs Production environments:"
echo "   # Development"
echo "   eval \$(bw-secrets inject \\"
echo "     --secret-keys \"dev-api-key,dev-db-password\" \\"
echo "     --secret-vars \"API_KEY,DB_PASSWORD\")"
echo
echo "   # Production"
echo "   eval \$(bw-secrets inject \\"
echo "     --secret-keys \"prod-api-key,prod-db-password\" \\"
echo "     --secret-vars \"API_KEY,DB_PASSWORD\")"
echo

# Example 9: Shell integration
echo "9. Shell integration (add to .bashrc/.zshrc):"
echo "   load_secrets() {"
echo "       eval \$(bw-secrets inject --quiet)"
echo "   }"
echo "   alias secrets='load_secrets'"
echo

echo "=== End of Examples ===" 
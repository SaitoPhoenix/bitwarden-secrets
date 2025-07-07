# Bitwarden Secrets CLI

A command-line tool for injecting Bitwarden secrets into your shell environment. This tool allows you to securely retrieve secrets from Bitwarden and set them as environment variables in your current shell session.

## Features

- 🔐 **Secure Secret Injection**: Retrieve secrets from Bitwarden and inject them as environment variables
- 🐚 **Multi-Shell Support**: Works with bash, zsh, fish, PowerShell, and Windows CMD
- 🎯 **Flexible Configuration**: Configure via environment variables or command-line options
- 📋 **Secret Listing**: List all available secrets in your Bitwarden organization
- ⚙️ **Configuration Management**: View and manage your current configuration
- 🔄 **Auto-Shell Detection**: Automatically detects your shell type for proper export formatting

## Installation

### Prerequisites

- Python 3.12+
- Bitwarden organization with secrets
- Bitwarden access token

### Install the Package

```bash
# Clone the repository
git clone <repository-url>
cd bitwarden-secrets

# Install with uv (recommended)
uv sync

# Or install with pip
pip install -e .
```

## Quick Start

### 1. Set up Environment Variables

Create a `.env` file or set environment variables:

```bash
# Required
export ORGANIZATION_ID="your-organization-id"
export ACCESS_TOKEN="your-access-token"
export SECRET_KEYS="api-key,database-password,redis-url"
export SECRET_VARS="API_KEY,DB_PASSWORD,REDIS_URL"

# Optional
export API_URL="https://api.bitwarden.com"
export IDENTITY_URL="https://identity.bitwarden.com"
```

### 2. Inject Secrets into Your Shell

```bash
# Basic usage - outputs export commands
eval $(bw-secrets inject)

# For PowerShell
bw-secrets inject --shell powershell | Invoke-Expression

# For fish shell
bw-secrets inject --shell fish | source
```

## Usage

### Main Commands

#### `bw-secrets inject`

Inject secrets from Bitwarden into your environment.

```bash
# Basic usage with environment variables
eval $(bw-secrets inject)

# Specify secrets directly
eval $(bw-secrets inject \
  --secret-keys "api-key,database-password" \
  --secret-vars "API_KEY,DB_PASSWORD")

# For PowerShell
bw-secrets inject --shell powershell | Invoke-Expression

# Quiet mode (suppress info messages)
eval $(bw-secrets inject --quiet)
```

**Options:**
- `--organization-id`: Bitwarden organization ID
- `--access-token`: Bitwarden access token
- `--secret-keys`: Comma-separated list of secret keys
- `--secret-vars`: Comma-separated list of environment variable names
- `--api-url`: Custom Bitwarden API URL
- `--identity-url`: Custom Bitwarden identity URL
- `--shell`: Shell type (bash, zsh, fish, powershell, cmd)
- `--quiet, -q`: Suppress informational messages

#### `bw-secrets list-secrets`

List all available secrets in your Bitwarden organization.

```bash
# List all secrets
bw-secrets list-secrets

# With custom configuration
bw-secrets list-secrets \
  --organization-id "your-org-id" \
  --access-token "your-token"
```

#### `bw-secrets config`

Show current configuration and environment variables.

```bash
bw-secrets config
```

**Output:**
```
Current Configuration:
  ORGANIZATION_ID: abc123...
  ACCESS_TOKEN: xyz789...
  SECRET_KEYS: api-key,database-password
  SECRET_VARS: API_KEY,DB_PASSWORD
  API_URL: https://api.bitwarden.com
  IDENTITY_URL: https://identity.bitwarden.com

Secret Mappings:
  api-key -> API_KEY
  database-password -> DB_PASSWORD
```

## Shell Integration

### Bash/Zsh

Add to your `.bashrc` or `.zshrc`:

```bash
# Function to load secrets
load_secrets() {
    eval $(bw-secrets inject --quiet)
}

# Alias for quick access
alias secrets='load_secrets'
```

### Fish Shell

Add to your `config.fish`:

```fish
# Function to load secrets
function load_secrets
    bw-secrets inject --shell fish | source
end

# Alias for quick access
alias secrets='load_secrets'
```

### PowerShell

Add to your PowerShell profile:

```powershell
# Function to load secrets
function Load-Secrets {
    bw-secrets inject --shell powershell | Invoke-Expression
}

# Alias for quick access
Set-Alias -Name secrets -Value Load-Secrets
```

## Configuration

### Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `ORGANIZATION_ID` | Yes | Bitwarden organization ID | - |
| `ACCESS_TOKEN` | Yes | Bitwarden access token | - |
| `SECRET_KEYS` | Yes | Comma-separated secret keys | - |
| `SECRET_VARS` | Yes | Comma-separated env var names | - |
| `API_URL` | No | Bitwarden API URL | `https://api.bitwarden.com` |
| `IDENTITY_URL` | No | Bitwarden identity URL | `https://identity.bitwarden.com` |

### Secret Mapping

The tool maps Bitwarden secret keys to environment variable names:

```bash
# Example mapping
SECRET_KEYS="api-key,database-password,redis-url"
SECRET_VARS="API_KEY,DB_PASSWORD,REDIS_URL"

# Results in:
# Bitwarden secret "api-key" → Environment variable "API_KEY"
# Bitwarden secret "database-password" → Environment variable "DB_PASSWORD"
# Bitwarden secret "redis-url" → Environment variable "REDIS_URL"
```

## Examples

### Development Environment Setup

```bash
# Load development secrets
eval $(bw-secrets inject \
  --secret-keys "dev-api-key,dev-db-password,dev-redis-url" \
  --secret-vars "API_KEY,DB_PASSWORD,REDIS_URL")
```

### Production Environment Setup

```bash
# Load production secrets
eval $(bw-secrets inject \
  --secret-keys "prod-api-key,prod-db-password,prod-redis-url" \
  --secret-vars "API_KEY,DB_PASSWORD,REDIS_URL")
```

### CI/CD Pipeline

```bash
# In your CI/CD script
bw-secrets inject --quiet | while read line; do
    echo "$line" >> $GITHUB_ENV
done
```

### Docker Container

```bash
# In your Dockerfile or docker-compose
RUN eval $(bw-secrets inject) && your-application
```

## Security Considerations

- **Access Tokens**: Store access tokens securely and rotate them regularly
- **Environment Variables**: Be careful not to log environment variables containing secrets
- **Shell History**: Consider using `--quiet` flag to reduce sensitive data in shell history
- **CI/CD**: Use secure secret management in CI/CD pipelines

## Troubleshooting

### Common Issues

1. **Authentication Failed**
   ```bash
   # Check your access token
   bw-secrets config
   ```

2. **Secrets Not Found**
   ```bash
   # List available secrets
   bw-secrets list-secrets
   ```

3. **Wrong Shell Format**
   ```bash
   # Specify shell explicitly
   bw-secrets inject --shell powershell
   ```

### Debug Mode

Enable debug logging by setting the log level:

```bash
export PYTHONPATH=.
python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from bitwarden_secrets.injector import inject_secrets
inject_secrets()
"
```

## Development

### Project Structure

```
bitwarden-secrets/
├── bitwarden_secrets/
│   ├── __init__.py
│   ├── injector.py      # Core BitwardenSecretsInjector class
│   └── cli.py          # CLI interface using Click
├── config_bitwarden.py  # Legacy entry point
├── pyproject.toml      # Project configuration
└── README.md
```

### Running Tests

```bash
# Install development dependencies
uv sync --group dev

# Run tests (when implemented)
pytest
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section above
- Review the Bitwarden SDK documentation

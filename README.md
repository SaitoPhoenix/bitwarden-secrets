# Bitwarden Secrets Injector

This project provides a Python script (`config-bitwarden.py`) to fetch secrets from Bitwarden Secrets Manager and inject them as environment variables into the current session.

## How it Works

*   Connects to Bitwarden using an API access token.
*   Authenticates and syncs secrets for a specified organization.
*   Retrieves specified secrets based on a mapping defined in environment variables.
*   Sets these secrets as environment variables.

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Create and activate a virtual environment using UV:**
    ```bash
    uv venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies using UV:**
    ```bash
    uv sync
    ```

4.  **Set up the `.env` file:**
    Create a `.env` file in the root of the project with the following variables:

    ```env
    # Required
    ORGANIZATION_ID="your_bitwarden_organization_id"
    ACCESS_TOKEN="your_bitwarden_sm_access_token"
    SECRET_KEYS="bitwarden_secret_name1,bitwarden_secret_name2"
    SECRET_VARS="ENV_VAR_NAME1,ENV_VAR_NAME2"

    # Optional - Defaults to Bitwarden cloud
    # API_URL="https://api.bitwarden.com"
    # IDENTITY_URL="https://identity.bitwarden.com"
    ```
    *   `ORGANIZATION_ID`: Your Bitwarden organization ID.
    *   `ACCESS_TOKEN`: Your Bitwarden Secrets Manager access token.
    *   `SECRET_KEYS`: Comma-separated list of the "key" names of the secrets as they appear in Bitwarden.
    *   `SECRET_VARS`: Comma-separated list of the environment variable names you want to map the secrets to. The order must correspond to `SECRET_KEYS`.
    *   `API_URL` (Optional): Override if using a self-hosted Bitwarden instance.
    *   `IDENTITY_URL` (Optional): Override if using a self-hosted Bitwarden instance.

## Usage

Once the `.env` file is configured and dependencies are installed, you can run the script:

```bash
python config-bitwarden.py
```

This will fetch the configured secrets and set them as environment variables in the current shell session where the script is executed. The script itself doesn't return any output upon success, but logs its actions to the console.

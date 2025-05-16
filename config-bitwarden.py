import logging
import os
import sys
from datetime import datetime, timezone
from dotenv import load_dotenv
from bitwarden_sdk import BitwardenClient, DeviceType, client_settings_from_dict

load_dotenv(override=True)


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class BitwardenSecretsManager:
    """
    Class to manage Bitwarden secrets and set them as environment variables.
    
    This class handles connecting to Bitwarden Secrets Manager, authentication,
    syncing secrets, and mapping them to environment variables.
    """
    
    def __init__(self):
        """Initialize the BitwardenSecretsManager."""
        self.client = self._create_client()
        self.organization_id = self.get_required_env_var("ORGANIZATION_ID")
        self.access_token = self.get_required_env_var("ACCESS_TOKEN")
        self.secrets_mapping = self._create_secrets_mapping()
        
    def _create_client(self):
        """
        Create and configure a Bitwarden client.
        
        Returns:
            BitwardenClient: Configured Bitwarden client instance
        """
        return BitwardenClient(
            client_settings_from_dict(
                {
                    "apiUrl": os.getenv("API_URL", "https://api.bitwarden.com"),
                    "deviceType": DeviceType.SDK,
                    "identityUrl": os.getenv(
                        "IDENTITY_URL", "https://identity.bitwarden.com"
                    ),
                    "userAgent": "Python",
                }
            )
        )
        
    def _create_secrets_mapping(self):
        """
        Create a mapping between secret keys and environment variable names.
        
        Returns:
            dict: Mapping of secret keys to environment variable names
        """
        # Get the secrets keys and environment variable names from environment variables
        secret_keys = [key.strip() for key in os.getenv("SECRET_KEYS", "").split(",")]
        secret_vars = [var.strip() for var in os.getenv("SECRET_VARS", "").split(",")]

        if not secret_keys[0] or not secret_vars[0]:
            logger.warning("No secret mappings provided in SECRET_KEYS or SECRET_VARS")

        # Create a dictionary mapping secrets keys to environment variable names
        secrets_mapping = {}
        for i in range(min(len(secret_keys), len(secret_vars))):
            key = secret_keys[i].strip()
            var = secret_vars[i].strip()
            if key and var:  # Only add non-empty pairs
                secrets_mapping[key] = var

        logger.info(f"Processing {len(secrets_mapping)} secret mappings")
        return secrets_mapping

    def get_required_env_var(self, name):
        """
        Get a required environment variable or exit if it doesn't exist.
        
        Args:
            name (str): The name of the environment variable to retrieve
            
        Returns:
            str: The value of the environment variable
            
        Exits:
            If the environment variable is not set, logs an error and exits
        """
        value = os.getenv(name)
        if not value:
            logger.error(f"Required environment variable {name} is not set")
            sys.exit(1)
        return value
            
    def authenticate(self):
        """
        Authenticate with Bitwarden using the access token.
        
        Returns:
            bool: True if authentication was successful, False otherwise
        """
        try:
            auth_result = self.client.auth().login_access_token(self.access_token)
            if not auth_result.success:
                logger.error(f"Authentication failed: {auth_result.error_message}")
                return False
            logger.info("Authentication successful")
            return True
        except Exception as e:
            logger.error(f"Authentication error: {str(e)}")
            return False
            
    def sync_secrets(self):
        """
        Sync secrets from Bitwarden.
        
        Returns:
            bool: True if sync was successful, False otherwise
        """
        try:
            sync_result = self.client.secrets().sync(
                self.organization_id, datetime.now(tz=timezone.utc)
            )
            if not sync_result.success:
                logger.error(f"Secrets sync failed: {sync_result.error_message}")
                return False
            logger.info("Secrets sync successful")
            return True
        except Exception as e:
            logger.error(f"Secrets sync error: {str(e)}")
            return False
    
    def list_secrets(self):
        """
        List all secrets from the organization.
        
        Returns:
            list: List of secrets if successful, None otherwise
        """
        try:
            secrets_list = self.client.secrets().list(self.organization_id)
            if not secrets_list.success:
                logger.error(f"Failed to list secrets: {secrets_list.error_message}")
                return None
                
            secrets_data = secrets_list.data.to_dict()["data"]
            logger.info(f"Found {len(secrets_data)} secrets in the organization")
            return secrets_data
        except Exception as e:
            logger.error(f"Error listing secrets: {str(e)}")
            return None
    
    def get_secret_value(self, secret_id):
        """
        Get the value of a specific secret.
        
        Args:
            secret_id (str): The ID of the secret to retrieve
            
        Returns:
            str: The secret value if successful, None otherwise
        """
        try:
            secret_response = self.client.secrets().get(secret_id)
            if secret_response.success and secret_response.data:
                return secret_response.data.value
            else:
                logger.error(f"Failed to retrieve secret: {secret_response.error_message}")
                return None
        except Exception as e:
            logger.error(f"Error retrieving secret: {str(e)}")
            return None
    
    def process_secrets(self):
        """
        Process secrets and set them as environment variables.
        
        Returns:
            tuple: (processed_count, total_count) - counts of processed secrets and total mappings
        """
        secrets_data = self.list_secrets()
        if not secrets_data:
            return 0, len(self.secrets_mapping)
            
        processed_secrets = 0
        for secret in secrets_data:
            # Check if this secret's key is in our mapping
            if secret["key"] in self.secrets_mapping:
                # Get the environment variable name from the mapping
                env_var_name = self.secrets_mapping[secret["key"]]
                # Get the secret value using its ID
                secret_value = self.get_secret_value(secret["id"])
                if secret_value:
                    # Set the environment variable with the secret's value
                    os.environ[env_var_name] = secret_value
                    logger.info(f"Set environment variable {env_var_name} from secret {secret['key']}")
                    processed_secrets += 1
                else:
                    logger.error(f"Could not set environment variable {env_var_name} from secret {secret['key']}")
                    
        return processed_secrets, len(self.secrets_mapping)
    
    def run(self):
        """
        Run the complete process to set environment variables from Bitwarden secrets.
        """
        try:
            # No secrets to process if mapping is empty
            if not self.secrets_mapping:
                logger.info("No secrets to process")
                return
                
            # Authenticate and sync
            if not self.authenticate():
                return
            if not self.sync_secrets():
                return
                
            # Process secrets
            processed_count, total_count = self.process_secrets()
            
            # Report results
            logger.info(f"Successfully processed {processed_count} out of {total_count} mapped secrets")
            missing_secrets = total_count - processed_count
            if missing_secrets > 0:
                logger.warning(f"{missing_secrets} mapped secrets were not found in the organization")
                
        except Exception as e:
            logger.error(f"Unexpected error in Bitwarden secrets processing: {str(e)}")


def set_managed_variables():
    """
    Connect to Bitwarden Secrets Manager and set environment variables from secrets.
    
    This function:
    1. Creates a Bitwarden client using environment configuration
    2. Authenticates using an access token
    3. Syncs secrets from the specified organization
    4. Maps secret values to environment variables according to SECRET_KEYS and SECRET_VARS
    
    Required environment variables:
        - ORGANIZATION_ID: Bitwarden organization identifier
        - ACCESS_TOKEN: Bitwarden Secrets Manager access token
        - SECRET_KEYS: Comma-separated list of secret keys to retrieve
        - SECRET_VARS: Comma-separated list of environment variable names to set
        
    Optional environment variables:
        - API_URL: Custom Bitwarden API URL (defaults to https://api.bitwarden.com)
        - IDENTITY_URL: Custom Bitwarden identity URL (defaults to https://identity.bitwarden.com)
    """
    manager = BitwardenSecretsManager()
    manager.run()


if __name__ == "__main__":
    set_managed_variables()

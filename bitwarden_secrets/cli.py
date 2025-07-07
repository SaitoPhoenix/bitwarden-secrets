#!/usr/bin/env python3
"""
Bitwarden Secrets CLI

A command-line interface for injecting Bitwarden secrets into the shell environment.
"""

import os
import sys
import click
from typing import Optional, List
from .injector import BitwardenSecretsInjector


@click.group()
@click.version_option(version="1.0.0")
def main():
    """
    Bitwarden Secrets CLI - Inject secrets from Bitwarden into your shell environment.

    This tool allows you to retrieve secrets from Bitwarden and inject them
    as environment variables into your current shell session.
    """
    pass


@main.command()
@click.option(
    "--organization-id",
    envvar="ORGANIZATION_ID",
    help="Bitwarden organization ID (can also be set via ORGANIZATION_ID env var)",
)
@click.option(
    "--access-token",
    envvar="ACCESS_TOKEN",
    help="Bitwarden access token (can also be set via ACCESS_TOKEN env var)",
)
@click.option(
    "--secret-keys",
    envvar="SECRET_KEYS",
    help="Comma-separated list of secret keys to retrieve (can also be set via SECRET_KEYS env var)",
)
@click.option(
    "--secret-vars",
    envvar="SECRET_VARS",
    help="Comma-separated list of environment variable names to set (can also be set via SECRET_VARS env var)",
)
@click.option(
    "--api-url",
    envvar="API_URL",
    default="https://api.bitwarden.com",
    help="Custom Bitwarden API URL (defaults to https://api.bitwarden.com)",
)
@click.option(
    "--identity-url",
    envvar="IDENTITY_URL",
    default="https://identity.bitwarden.com",
    help="Custom Bitwarden identity URL (defaults to https://identity.bitwarden.com)",
)
@click.option(
    "--shell",
    type=click.Choice(["bash", "zsh", "fish", "powershell", "cmd"]),
    help="Shell type for export format (auto-detected if not specified)",
)
@click.option(
    "--eval",
    is_flag=True,
    help="Output shell commands that can be evaluated (e.g., eval $(bw-secrets inject --eval))",
)
@click.option(
    "--quiet",
    "-q",
    is_flag=True,
    help="Suppress informational messages",
)
def inject(
    organization_id: Optional[str],
    access_token: Optional[str],
    secret_keys: Optional[str],
    secret_vars: Optional[str],
    api_url: str,
    identity_url: str,
    shell: Optional[str],
    eval: bool,
    quiet: bool,
):
    """
    Inject Bitwarden secrets into the environment.

    This command retrieves secrets from Bitwarden and outputs export commands
    that can be sourced into your shell environment.

    Examples:
        # Basic usage with environment variables
        eval $(bw-secrets inject)

        # Specify secrets directly
        eval $(bw-secrets inject --secret-keys "api-key,database-password" --secret-vars "API_KEY,DB_PASSWORD")

        # For PowerShell
        bw-secrets inject --shell powershell | Invoke-Expression
    """
    # Set environment variables from CLI options if provided
    if organization_id:
        os.environ["ORGANIZATION_ID"] = organization_id
    if access_token:
        os.environ["ACCESS_TOKEN"] = access_token
    if secret_keys:
        os.environ["SECRET_KEYS"] = secret_keys
    if secret_vars:
        os.environ["SECRET_VARS"] = secret_vars
    if api_url:
        os.environ["API_URL"] = api_url
    if identity_url:
        os.environ["IDENTITY_URL"] = identity_url

    # Configure logging level
    if quiet:
        import logging

        logging.getLogger().setLevel(logging.ERROR)

    # Auto-detect shell if not specified
    if not shell:
        shell = _detect_shell()

    try:
        # Create injector and run
        injector = BitwardenSecretsInjector()

        # Override the process_secrets method to use the correct shell format
        original_process_secrets = injector.process_secrets

        def process_secrets_with_shell():
            secrets_data = injector.list_secrets()
            if not secrets_data:
                return 0, len(injector.secrets_mapping)

            processed_secrets = 0
            for secret in secrets_data:
                if secret["key"] in injector.secrets_mapping:
                    env_var_name = injector.secrets_mapping[secret["key"]]
                    secret_value = injector.get_secret_value(secret["id"])
                    if secret_value:
                        os.environ[env_var_name] = secret_value
                        # Output shell-specific export command
                        print(_format_export_command(env_var_name, secret_value, shell))
                        if not quiet:
                            click.echo(
                                f"Set {env_var_name} from secret {secret['key']}",
                                err=True,
                            )
                        processed_secrets += 1
                    else:
                        if not quiet:
                            click.echo(
                                f"Could not retrieve secret {secret['key']}", err=True
                            )

            return processed_secrets, len(injector.secrets_mapping)

        injector.process_secrets = process_secrets_with_shell
        injector.run()

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
@click.option(
    "--organization-id",
    envvar="ORGANIZATION_ID",
    help="Bitwarden organization ID (can also be set via ORGANIZATION_ID env var)",
)
@click.option(
    "--access-token",
    envvar="ACCESS_TOKEN",
    help="Bitwarden access token (can also be set via ACCESS_TOKEN env var)",
)
@click.option(
    "--api-url",
    envvar="API_URL",
    default="https://api.bitwarden.com",
    help="Custom Bitwarden API URL",
)
@click.option(
    "--identity-url",
    envvar="IDENTITY_URL",
    default="https://identity.bitwarden.com",
    help="Custom Bitwarden identity URL",
)
def list_secrets(
    organization_id: Optional[str],
    access_token: Optional[str],
    api_url: str,
    identity_url: str,
):
    """
    List all available secrets in the Bitwarden organization.

    This command shows all secrets that are available for injection,
    along with their keys and creation dates.
    """
    # Set environment variables from CLI options if provided
    if organization_id:
        os.environ["ORGANIZATION_ID"] = organization_id
    if access_token:
        os.environ["ACCESS_TOKEN"] = access_token
    if api_url:
        os.environ["API_URL"] = api_url
    if identity_url:
        os.environ["IDENTITY_URL"] = identity_url

    try:
        injector = BitwardenSecretsInjector()

        if not injector.authenticate():
            click.echo("Authentication failed", err=True)
            sys.exit(1)

        if not injector.sync_secrets():
            click.echo("Failed to sync secrets", err=True)
            sys.exit(1)

        secrets_data = injector.list_secrets()
        if not secrets_data:
            click.echo("No secrets found in the organization")
            return

        click.echo(f"Found {len(secrets_data)} secrets in the organization:")
        click.echo()

        for secret in secrets_data:
            click.echo(f"  Key: {secret['key']}")
            click.echo(f"  ID: {secret['id']}")
            click.echo(f"  Created: {secret.get('creationDate', 'Unknown')}")
            click.echo(f"  Updated: {secret.get('revisionDate', 'Unknown')}")
            click.echo()

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        sys.exit(1)


@main.command()
def config():
    """
    Show current configuration and environment variables.

    This command displays the current configuration that would be used
    for secret injection, including which environment variables are set.
    """
    config_vars = {
        "ORGANIZATION_ID": os.getenv("ORGANIZATION_ID"),
        "ACCESS_TOKEN": os.getenv("ACCESS_TOKEN"),
        "SECRET_KEYS": os.getenv("SECRET_KEYS"),
        "SECRET_VARS": os.getenv("SECRET_VARS"),
        "API_URL": os.getenv("API_URL", "https://api.bitwarden.com"),
        "IDENTITY_URL": os.getenv("IDENTITY_URL", "https://identity.bitwarden.com"),
    }

    click.echo("Current Configuration:")
    click.echo()

    for var, value in config_vars.items():
        if var == "ACCESS_TOKEN" and value:
            # Mask the access token for security
            masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            click.echo(f"  {var}: {masked_value}")
        else:
            click.echo(f"  {var}: {value or 'Not set'}")

    click.echo()

    # Show secret mappings if available
    if config_vars["SECRET_KEYS"] and config_vars["SECRET_VARS"]:
        secret_keys = [key.strip() for key in config_vars["SECRET_KEYS"].split(",")]
        secret_vars = [var.strip() for var in config_vars["SECRET_VARS"].split(",")]

        click.echo("Secret Mappings:")
        for i in range(min(len(secret_keys), len(secret_vars))):
            if secret_keys[i] and secret_vars[i]:
                click.echo(f"  {secret_keys[i]} -> {secret_vars[i]}")


def _detect_shell() -> str:
    """Detect the current shell type."""
    shell = os.getenv("SHELL", "").lower()
    if "bash" in shell:
        return "bash"
    elif "zsh" in shell:
        return "zsh"
    elif "fish" in shell:
        return "fish"
    elif "powershell" in shell or "pwsh" in shell:
        return "powershell"
    elif os.name == "nt":  # Windows
        return "cmd"
    else:
        return "bash"  # Default fallback


def _format_export_command(var_name: str, value: str, shell: str) -> str:
    """Format an export command for the specified shell."""
    # Escape the value for shell safety
    escaped_value = value.replace('"', '\\"').replace("'", "\\'")

    if shell in ["bash", "zsh"]:
        return f'export {var_name}="{escaped_value}"'
    elif shell == "fish":
        return f'set -gx {var_name} "{escaped_value}"'
    elif shell == "powershell":
        return f'$env:{var_name} = "{escaped_value}"'
    elif shell == "cmd":
        return f"set {var_name}={escaped_value}"
    else:
        return f'export {var_name}="{escaped_value}"'  # Default to bash format


if __name__ == "__main__":
    main()

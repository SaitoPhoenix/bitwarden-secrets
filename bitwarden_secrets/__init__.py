"""
Bitwarden Secrets Injector

A Python package for injecting Bitwarden secrets into environment variables.
"""

from .injector import BitwardenSecretsInjector, inject_secrets

__version__ = "1.0.0"
__all__ = ["BitwardenSecretsInjector", "inject_secrets"]

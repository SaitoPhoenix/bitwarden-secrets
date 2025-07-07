#!/usr/bin/env python3
"""
Bitwarden Secrets Configuration - Legacy Entry Point

This file maintains backward compatibility with the original script.
For new usage, consider using the CLI tool: bw-secrets
"""

from bitwarden_secrets.injector import inject_secrets

if __name__ == "__main__":
    inject_secrets()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generate Postgres-backed v1 application authentication credentials.

This utility prints:
- the raw JWT token to send as `x-api-key`
- the bcrypt hash to store in `applications.api_key`
- a ready-to-run SQL update statement
- a sample curl command for testing the protected v1 routes
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core.auth import build_application_api_credentials


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate v1 application JWT and DB hash for Postgres auth.")
    parser.add_argument("--app-id", required=True,
                        help="Existing applications.id value in Postgres")
    parser.add_argument("--app-name", required=True,
                        help="Existing applications.name value in Postgres")
    parser.add_argument(
        "--base-url",
        default="http://127.0.0.1:8000",
        help="Base URL for the sample curl command",
    )
    return parser.parse_args()


def main() -> None:
    """Generate the raw JWT and hashed API key for a v1 application."""
    args = parse_args()
    raw_jwt, hashed_api_key = build_application_api_credentials(
        app_name=args.app_name,
        app_id=args.app_id,
    )

    print("RAW_JWT_USE_THIS_IN_X_API_KEY=")
    print(raw_jwt)
    print()
    print("HASHED_API_KEY_STORE_THIS_IN_POSTGRES=")
    print(hashed_api_key)
    print()
    print("SQL_UPDATE=")
    print(
        f"UPDATE applications\n"
        f"SET api_key = '{hashed_api_key}',\n"
        f"    deleted_at = NULL,\n"
        f"    is_active = TRUE\n"
        f"WHERE id = '{args.app_id}';"
    )
    print()
    print("TEST_COMMAND=")
    print(
        f"curl -i \\\n"
        f"  -H \"x-api-key: {raw_jwt}\" \\\n"
        f"  {args.base_url}/api/v1/users"
    )


if __name__ == "__main__":
    main()


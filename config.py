"""
This module provides a function to load configuration
variables from environment variables. It also attempts
to load these from a .env file if it exists.
"""

import os
from dotenv import load_dotenv

ENV_PATH = ".env"

if os.path.exists(ENV_PATH):
    load_dotenv(ENV_PATH)

TOKEN = os.getenv("DISCORD_TOKEN")
DATABASE_FILE = os.getenv("DB_PATH")
BUILD_VERSION = os.getenv("BUILD_VERSION", "default-value")

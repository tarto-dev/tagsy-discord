"""
This module provides a function to load configuration
variables from environment variables. It also attempts
to load these from a .env file if it exists.
"""

import os
from dotenv import load_dotenv

env_path = ".env"

if os.path.exists(env_path):
    load_dotenv(env_path)

TOKEN = os.getenv("DISCORD_TOKEN")

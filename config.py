"""
This module provides a function to load configuration
variables from environment variables and a .env file.
"""

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

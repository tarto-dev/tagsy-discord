from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the DISCORD_TOKEN variable
TOKEN = os.getenv("DISCORD_TOKEN")

import disnake
from disnake.ext import commands
import os
from db import db_setup
import config

intents = disnake.Intents.all()
intents.presences = False

bot = commands.Bot(intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    await db_setup()  # Initialise la base de données

    for filename in os.listdir("./commands"):
        if filename.endswith(".py") and not filename.startswith("_"):
            extension = filename[:-3]
            try:
                bot.load_extension(f"commands.{extension}")
                print(f"Loaded extension: {extension}")
            except Exception as e:
                print(f"Failed to load extension {extension}.", e)


bot.run(config.TOKEN)

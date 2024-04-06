# -*- coding: utf-8 -*-
"""
This is a Discord bot implemented using the disnake library.

It handles various events and commands for interaction on a Discord server.
"""

import os

import disnake
from disnake.ext import commands

import config
from db import db_setup

intents = disnake.Intents.all()
intents.presences = False

bot = commands.Bot(intents=intents, command_prefix="!!!", help_command=None)


@bot.event
async def on_ready():
    """
    Event handler that is called when the bot is ready to start receiving events from
    Discord.

    This function prints a message to indicate that the bot has connected to Discord and then
    initializes the database.
    It also loads all the command extensions from the "./commands" directory.

    Args:
        None

    Returns:
        None
    """
    print(f"{bot.user} has connected to Discord!")
    await db_setup()  # Setup the database

    for filename in os.listdir("./commands"):
        if filename.endswith(".py") and not filename.startswith("_"):
            extension = filename[:-3]
            try:
                bot.load_extension(f"commands.{extension}")
                print(f"Loaded extension: {extension}")
            except commands.errors.ExtensionNotFound as e:
                print(f"Failed to load extension {extension}.", e)


bot.run(config.TOKEN)

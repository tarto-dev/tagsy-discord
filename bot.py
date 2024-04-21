# -*- coding: utf-8 -*-
"""
This is a Discord bot implemented using the disnake library.

It handles various events and commands for interaction on a Discord server.
"""

import os

import disnake
import sentry_sdk
from disnake.ext import commands

import config
from context_menu import ContextMenuCommands
from db.sqlite_handler import db_setup
from helper import sentry_capture

sentry_sdk.init(
    dsn=config.SENTRY_DSN,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)

intents = disnake.Intents.all()
intents.presences = False

bot = commands.Bot(
    intents=intents,
    command_prefix="!!!",
    help_command=None,
    command_sync_flags=commands.CommandSyncFlags.all(),
)


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
                sentry_capture(
                    commands.errors.ExtensionNotFound(
                        f"Extension not found: {extension}"
                    ),
                    0,
                    0,
                )
                print(f"Failed to load extension {extension}.", e)
    bot.add_cog(ContextMenuCommands(bot))


bot.run(config.TOKEN)

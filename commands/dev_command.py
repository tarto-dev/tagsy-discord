"""
This module contains the implementation of the dev command.

This module provides functionality to download the database dump.
"""

import csv
from io import StringIO
import disnake
from disnake.ext import commands

from db import get_all_tags_for_all_servers


class DevCommands(commands.Cog):
    """
    A class that represents development commands for the bot.
    These commands are only available to the bot owner.
    """

    def __init__(self, bot):
        """
        Initializes a new instance of the DevCommand class.

        Args:
            bot: The bot instance.

        Returns:
            None
        """
        self.bot = bot

    @commands.command(name="senddb", hidden=True)
    @commands.is_owner()
    async def send_database(self, ctx):
        """
        Sends the database file to the bot owner via direct message.
        This command is only available to the bot owner.

        Parameters:
        - ctx (commands.Context): The context object representing the invocation context.

        Raises:
        - FileNotFoundError: If the database file is not found.
        - disnake.Forbidden: If the bot doesn't have permission to send direct messages to the user.
        - disnake.HTTPException: If an error occurs while sending the file.

        Returns:
        - None
        """
        try:
            with open("/app/data/database.db", "rb") as db_file:
                await ctx.author.send(
                    "Here is the database file:",
                    file=disnake.File(db_file, "database.db"),
                )
        except FileNotFoundError:
            await ctx.send("The file was not found.", ephemeral=True)
        except disnake.Forbidden:
            await ctx.send(
                "I don't have permission" + " to send direct messages to this user.",
                ephemeral=True,
            )
        except disnake.HTTPException:
            await ctx.send("An error occurred while sending the file.", ephemeral=True)

    @commands.command(name="reload", hidden=True)
    @commands.is_owner()
    async def reload_extension(self, ctx, extension):
        """
        Reloads a command extension.
        This command is only available to the bot owner.

        Args:
            extension (str): The name of the extension to reload.

        Raises:
            commands.errors.ExtensionNotFound: If the specified extension is not found.

        Returns:
            None
        """
        try:
            self.bot.reload_extension(f"commands.{extension}")
            await ctx.send(f"Extension reloaded: {extension}")
        except commands.errors.ExtensionNotFound as e:
            await ctx.send(f"Failed to reload extension {extension}. {e}")

    # command import database
    @commands.command(name="importdb", hidden=True)
    @commands.is_owner()
    async def import_database(self, ctx):
        """
        Imports the database file from the bot owner via direct message.
        This command is only available to the bot owner.

        Parameters:
        - ctx (disnake.Context): The context object representing the invocation of the command.

        Raises:
        - disnake.HTTPException: If there is an error while downloading the attachment.
        - IOError: If there is an error while saving the file.

        Returns:
        - None

        """
        try:
            attachment = ctx.message.attachments[0]
            if attachment.filename.endswith(".db"):
                await attachment.save(f"/app/data/{attachment.filename}")
                await ctx.send("Database file imported.")
            else:
                await ctx.send("Invalid file format. Please upload a .db file.")
        except disnake.HTTPException as e:
            await ctx.send(f"Failed to download the attachment: {e}")
        except IOError as e:
            await ctx.send(f"Failed to save the file: {e}")

    @commands.command(name="dumpcsv", hidden=True)
    @commands.is_owner()
    async def dump_csv(self, ctx):
        """
        Dumps all tags from all servers into a CSV file, including server ID, tag, content,
        created by, creation date, and usage count, then sends this file to the bot owner.

        Parameters:
        - ctx (commands.Context): The context of the command.

        Raises:
        - IOError: If there is an error creating or sending the file.
        - KeyError: If there is a data format error.
        - disnake.HTTPException: If there is an error sending the file via DM.
        """
        try:
            tags_data = await get_all_tags_for_all_servers()
            with StringIO() as output:
                writer = csv.writer(output)
                # Write the header of the CSV file
                writer.writerow(
                    [
                        "Server ID",
                        "Tag",
                        "Content",
                        "Created By",
                        "Created At",
                        "Usage Count",
                    ]
                )

                # Write each row from the tags_data dictionary
                for tag in tags_data:
                    writer.writerow(
                        [
                            tag["server_id"],
                            tag["tag"],
                            tag["content"],
                            tag["created_by"],
                            tag["created_at"],
                            tag["usage_count"],
                        ]
                    )

                output.seek(0)  # Go back to the start of the StringIO object
                # Send the generated CSV file
                await ctx.author.send(
                    "Here is the CSV dump of all tags:",
                    file=disnake.File(fp=output, filename="tags_dump.csv"),
                )

            await ctx.send("CSV dump of tags has been sent via DM.")
        except IOError as e:
            await ctx.send(f"Failed to create or send the file: {e}")
        except KeyError as e:
            await ctx.send(f"Data format error: Missing {e}")
        except disnake.HTTPException as e:
            await ctx.send(f"Failed to send file via DM: {e}")


def setup(bot):
    """
    Set up the bot by adding the DevCommands cog.

    Parameters:
    - bot: The bot instance.

    Returns:
    - None
    """
    bot.add_cog(DevCommands(bot))
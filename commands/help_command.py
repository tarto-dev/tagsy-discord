"""
This module provides a HelpCommands cog for a Discord bot.

The HelpCommands cog includes a help command that displays detailed information
about other commands available in the bot.

Users can invoke the help command without arguments
to get a list of all commands, or they can specify a command to get detailed
help for that command.

This cog is designed to enhance user experience by providing easy access
to command documentation directly within Discord.
"""

import disnake
from disnake.ext import commands


class HelpCommands(commands.Cog):
    """
    A Cog for displaying detailed help for the available commands in the bot.
    """

    def __init__(self, bot):
        """
        Initializes the HelpCommands cog.

        Args:
            bot: The bot instance that the cog is being added to.

        Attributes:
            bot: The bot instance that the cog is being added to.
        """
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx, *, command: str = None):
        """
        Displays help for all commands or for a specific command.

        Args:
            ctx: The command context.
            command: (Optional) The specific command to display help for.
        """
        if command is None:
            await self._show_all_commands(ctx)
        else:
            await self._show_command_help(ctx, command)

    async def _show_all_commands(self, ctx):
        """
        Displays help for all commands.

        Args:
            ctx: The command context.
        """
        embed = disnake.Embed(title="Available Commands", color=disnake.Color.blue())
        embed.add_field(
            name="Tag Commands",
            value="`/add`, `/get`, `/getall`, `/remove`, `/update`, `/reset`",
            inline=False,
        )
        if commands.is_owner():
            embed.add_field(
                name="Development Commands",
                value="`senddb`, `reload`, `importdb`, `dumpcsv`, `dumpconfig`",
                inline=False,
            )
        embed.set_footer(
            text="Use /help <command> for more info on a specific command."
        )
        await ctx.send(embed=embed)

    async def _show_command_help(self, ctx, command):
        """
        Displays help for a specific command.

        Args:
            ctx: The command context.
            command: The specific command to display help for.
        """
        commands_descriptions = {
            "add": "Adds a tagged message to the database."
            + " Usage: `/add <tag> <message>`",
            "get": "Retrieves and displays a tagged message." + " Usage: `/get <tag>`",
            "getall": "Retrieves all tagged messages with details."
            + " Usage: `/getall`",
            "remove": "Deletes a tagged message." + " Usage: `/remove <tag>`",
            "update": "Updates the content of a tagged message. "
            + " Usage: `/update <tag> <new message>`",
            "reset": "Resets the usage count for a tag." + " Usage: `/reset <tag>`",
        }

        description = commands_descriptions.get(command, "Command not found.")
        embed = disnake.Embed(
            title=f"Help for command: {command}",
            description=description,
            color=disnake.Color.green(),
        )
        await ctx.send(embed=embed)


def setup(bot):
    """
    Adds the HelpCommands cog to the bot.

    Args:
        bot: The bot instance.

    Returns:
        None
    """
    bot.add_cog(HelpCommands(bot))

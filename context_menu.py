# -*- coding: utf-8 -*-
"""This module contains the implementation of context menu commands for the bot."""

import disnake
from disnake.ext import commands

from helper import create_selected_message_content
from modals import AddTagModal


class ContextMenuCommands(commands.Cog):
    """A class that represents the context menu commands for the bot."""

    def __init__(self, bot):
        self.bot = bot

    @commands.message_command(name="Add as Tag")
    async def add_as_tag(self, inter: disnake.MessageCommandInteraction):
        """
        A context menu command that opens a modal for adding a tag based on the
        selected message.

        Parameters:
        - inter (disnake.MessageCommandInteraction):
            The interaction object representing the context menu interaction.

        Returns:
        - None

        Raises:
        - None
        """
        modal = AddTagModal(
            server_id=inter.guild_id,
            prefill_message=create_selected_message_content(inter),
        )
        await inter.response.send_modal(modal)

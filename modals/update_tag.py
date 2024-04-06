# -*- coding: utf-8 -*-
"""This module contains the modal classes used in the Tagsy application."""
# pylint: disable=arguments-differ,duplicate-code
import disnake

from db import get_similar_tags, update_message
from helper import tag_exists
from views import YesNoView


class UpdateTagModal(disnake.ui.Modal):
    """
    A modal for updating an existing tag.

    Args:
        server_id (int): The ID of the server where the tag exists.
    Attributes:
        server_id (int): The ID of the server where the tag exists.
    """

    def __init__(self, server_id):
        self.server_id = server_id
        components = [
            disnake.ui.TextInput(
                label="Tag",
                custom_id="tag",
                style=disnake.TextInputStyle.short,
                placeholder="Enter tag name",
                max_length=50,
                min_length=3,
            ),
            disnake.ui.TextInput(
                label="Message",
                custom_id="message",
                style=disnake.TextInputStyle.paragraph,
                placeholder="Enter the message for the tag",
                max_length=1024,
            ),
        ]
        super().__init__(title="Update existing Tag", components=components)

    async def callback(self, interaction: disnake.ModalInteraction):
        """
        Callback method called when the modal is interacted with.

        Args:
            interaction (disnake.ModalInteraction):
                The interaction object representing the user's interaction with the modal.
        """
        tag = interaction.text_values["tag"]
        message = interaction.text_values["message"]
        exists = await tag_exists(self.server_id, tag)

        if not exists:
            similar_tags = await get_similar_tags(self.server_id, tag)
            if similar_tags:
                suggestions = ", ".join([tag[0] for tag in similar_tags])
                await interaction.response.send_message(
                    f"The tag `{tag}` does not exist. "
                    + f"Did you mean: {suggestions}? Use /add to create a new tag.",
                    ephemeral=True,
                )
            else:
                await interaction.response.send_message(
                    f"The tag `{tag}` does not exist. Use /add to create it first.",
                    ephemeral=True,
                )
        else:
            if "\n" in message:
                view = YesNoView(
                    tag,
                    message,
                    action="update",
                    server_id=self.server_id,
                )
                await interaction.response.send_message(
                    "Do you want to update the message as a block code?",
                    view=view,
                    ephemeral=True,
                )
            else:
                await update_message(self.server_id, tag, message)
                await interaction.response.send_message(
                    f"Tag `{tag}` updated with message: {message}",
                    ephemeral=True,
                )

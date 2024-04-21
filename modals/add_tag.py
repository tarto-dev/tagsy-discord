# -*- coding: utf-8 -*-
"""This module contains the modal classes used in the Tagsy application."""
# pylint: disable=arguments-differ,duplicate-code

import disnake

from db.sqlite_handler import add_message
from helper import generate_recommendations, tag_exists
from views import YesNoView


class AddTagModal(disnake.ui.Modal):
    """A modal for adding a new tag."""

    def __init__(self, server_id, prefill_message=""):
        """
        Initialize the AddTagModal.

        Args:
            server_id (int): The ID of the server where the tag will be added.
        """
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
                value=prefill_message,
            ),
        ]
        super().__init__(title="Create Tag", components=components)

    async def callback(self, interaction: disnake.ModalInteraction):
        tag = interaction.text_values["tag"]
        message = interaction.text_values["message"]
        exists = await tag_exists(self.server_id, tag)

        if exists:
            recommendations = generate_recommendations(tag)
            recommendations_str = ", ".join(recommendations)
            await interaction.response.send_message(
                f"The tag `{tag}` already exists. Suggestions: {recommendations_str}.",
                ephemeral=True,
            )
        else:
            if "\n" in message:
                view = YesNoView(
                    tag,
                    message,
                    action="add",
                    user_id=str(interaction.user.id),
                    server_id=self.server_id,
                )
                await interaction.response.send_message(
                    "Do you want to add the message as a block code?",
                    view=view,
                    ephemeral=True,
                )
            else:
                await add_message(
                    self.server_id, tag, message, str(interaction.user.id)
                )
                await interaction.response.send_message(
                    f"Tag `{tag}` added with message: {message}", ephemeral=True
                )

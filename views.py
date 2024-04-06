# -*- coding: utf-8 -*-
"""_summary_.

This module contains the `YesNoView` class, which is a custom view for
displaying a yes/no confirmation prompt in a Discord interaction.

Classes:
- YesNoView: A custom view for displaying a yes/no confirmation prompt.
"""

import disnake

from db import add_message, update_message


class YesNoView(disnake.ui.View):
    """A custom view for displaying a yes/no confirmation prompt.

    This view provides two buttons: "Yes" and "No".
    When the "Yes" button is clicked,
    it performs the specified action (add or update) based on the provided parameters.

    When the "No" button is clicked,
    it performs the opposite action.

    Attributes:
    - tag (str): The tag associated with the confirmation prompt.

    - message (str): The message associated with the confirmation prompt.

    - action (str): The action to perform when the "Yes"
    button is clicked. Can be "add" or "update".

    - user_id (Optional[int]): The ID of the user who initiated
    the confirmation prompt. Defaults to None.

    - server_id (Optional[int]): The ID of the server where the
    confirmation prompt is displayed. Defaults to None.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, tag, message, action="add", user_id=None, server_id=None):
        super().__init__()
        self.tag = tag
        self.message = message
        self.action = action
        self.user_id = user_id
        self.server_id = server_id

    @disnake.ui.button(
        label="Yes", style=disnake.ButtonStyle.green, custom_id="yes_button"
    )
    async def confirm_yes(self, interaction: disnake.Interaction):
        """Callback function for the "Yes" button.

        This function is called when the "Yes" button is clicked.
        It performs the specified action (add or update)
        based on the provided parameters.

        Args:
        - button (disnake.ui.Button): The clicked button.

        - interaction (disnake.Interaction):
        The interaction object representing the user's interaction with the view.
        """
        message = f"```\n{self.message}\n```"
        if self.action == "add":
            await add_message(self.server_id, self.tag, message, self.user_id)
            await interaction.response.send_message(
                f"Tag `{self.tag}` added with message: {message}", ephemeral=True
            )
        elif self.action == "update":
            await update_message(self.server_id, self.tag, message)
            await interaction.response.send_message(
                f"Tag `{self.tag}` updated with message: {message}", ephemeral=True
            )
        self.stop()

    @disnake.ui.button(label="No", style=disnake.ButtonStyle.red, custom_id="no_button")
    async def confirm_no(self, interaction: disnake.Interaction):
        """Callback function for the "No" button.

        This function is called when the "No" button is clicked.
        It performs the opposite action of the specified action
        (add or update) based on the provided parameters.

        Args:
        - button (disnake.ui.Button): The clicked button.

        - interaction (disnake.Interaction):
        The interaction object representing the user's interaction with the view.
        """
        if self.action == "add":
            await add_message(self.server_id, self.tag, self.message, self.user_id)
            await interaction.response.send_message(
                f"Tag `{self.tag}` added with message: {self.message}", ephemeral=True
            )
        elif self.action == "update":
            await update_message(self.server_id, self.tag, self.message)
            await interaction.response.send_message(
                f"Tag `{self.tag}` updated with message: {self.message}", ephemeral=True
            )
        self.stop()

# -*- coding: utf-8 -*-
import disnake

from db import add_message, tag_exists, update_message


class YesNoView(disnake.ui.View):
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
    async def confirm_yes(
        self, button: disnake.ui.Button, interaction: disnake.Interaction
    ):
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
    async def confirm_no(
        self, button: disnake.ui.Button, interaction: disnake.Interaction
    ):
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

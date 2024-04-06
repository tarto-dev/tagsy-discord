# -*- coding: utf-8 -*-
"""A module that contains the TagCommands class,
which is a Cog for handling commands related to tagging messages within Discord servers.

This module provides functionality to add, retrieve, update, delete,
and reset tagged messages in a database.

Classes:
- TagCommands:
A Cog for handling commands related to tagging messages within Discord servers.
"""

import disnake
from disnake.ext import commands

from db import (
    delete_message,
    get_all_messages,
    get_message,
    get_similar_tags,
    increment_usage_count,
    reset_usage_count,
)

# Import functions from the database module to interact with tagged messages.
from helpers import build_embed, find_tag_in_string, tag_exists
from modals import AddTagModal, UpdateTagModal


class TagCommands(commands.Cog):
    """
    A Cog for handling commands related to tagging messages within Discord
    servers.
    """

    def __init__(self, bot):
        """
        Initializes the TagCommand class.

        Args:
            bot (Bot): The bot instance.

        Returns:
            None
        """
        self.bot = bot

    @commands.slash_command(name="add", description="Adds a new tag.")
    async def add(self, inter: disnake.ApplicationCommandInteraction):
        """
        Adds a new tag.

        Parameters:
        - inter: The disnake.ApplicationCommandInteraction object representing the interaction.

        Returns:
        - None

        Raises:
        - None
        """
        await inter.response.send_modal(AddTagModal(server_id=str(inter.guild.id)))

    @commands.slash_command(name="get", description="Retrieves a tagged message.")
    async def get(self, inter: disnake.ApplicationCommandInteraction, tag: str):
        """
        Retrieves and displays a tagged message from the database.

        If not found, suggests similar tags.

        Parameters:
        - inter: The interaction object representing the slash command interaction.
        - tag: The tag to retrieve.

        Returns:
        - None

        Raises:
        - disnake.NotFound: If the user who created the tagged message is not found.
        """
        server_id = str(inter.guild.id)
        tag_info = await get_message(server_id, tag)

        if tag_info:
            try:
                member = await inter.guild.fetch_member(int(tag_info["created_by"]))
                username = member.display_name
            except disnake.NotFound:
                username = "Unknown user"

            embed = build_embed(tag_info, username)
            await increment_usage_count(server_id, tag)
            await inter.response.send_message(embed=embed)
        else:
            echo = await get_similar_tags(server_id, tag)
            if echo:
                suggestions = ", ".join([str(e[0]) for e in echo])
                await inter.response.send_message(
                    f'No message found for tag "{tag}". Suggestions: {suggestions}',
                    ephemeral=True,
                )

    @commands.slash_command(
        name="getall", description="Retrieves all tagged messages with details."
    )
    async def getall(self, inter: disnake.ApplicationCommandInteraction):
        """
        Retrieves and displays all tags and their associated messages
        from the database for the server, including details such as.

        who posted it, when it was posted, and the number of uses.

        Each tagged message is displayed in its own embed.

        Parameters:
        - inter (disnake.ApplicationCommandInteraction):
        The interaction object representing the slash command interaction.

        Returns:
        None
        """
        server_id = str(inter.guild.id)
        tags_details = await get_all_messages(
            server_id
        )  # Assure this returns detailed info for each tag

        if tags_details:
            for detail in tags_details:
                # Fetch the username from the user ID
                try:
                    member = await inter.guild.fetch_member(int(detail["created_by"]))
                    username = member.display_name
                except disnake.NotFound:
                    username = "Unknown user"

                embed = build_embed(detail, username)
                # Check if it's the initial response or a follow-up
                if inter.response.is_done():
                    await inter.followup.send(embed=embed, ephemeral=True)
                else:
                    await inter.response.send_message(embed=embed, ephemeral=True)
        else:
            if not inter.response.is_done():
                await inter.response.send_message("No tags found.", ephemeral=True)
            else:
                await inter.followup.send("No tags found.", ephemeral=True)

    @commands.slash_command(name="remove", description="Deletes a tagged message.")
    async def remove(self, inter: disnake.ApplicationCommandInteraction, tag: str):
        """
        Deletes a tagged message from the database if the user
        has the required permissions.

        Parameters:
        - inter: The disnake.ApplicationCommandInteraction object
        representing the interaction with the slash command.
        - tag: The tag to be deleted.

        Returns:
        - None

        Raises:
        - None
        """
        server_id = str(inter.guild.id)

        if await tag_exists(server_id, tag):
            member = inter.guild.get_member(inter.author.id)
            if member.guild_permissions.manage_messages:
                await delete_message(server_id, tag)
                await inter.response.send_message(f'Tag "{tag}" deleted successfully.')
            else:
                await inter.response.send_message(
                    "You do not have permission to delete this tag.", ephemeral=True
                )
        else:
            echo = await get_similar_tags(server_id, tag)
            if echo:
                suggestions = [str(e[0]) for e in echo]
                await inter.response.send_message(
                    f"No message found for tag \"{tag}\". Suggestions: {', '.join(suggestions)}",
                    ephemeral=True,
                )
            else:
                await inter.response.send_message(
                    f'No message found for tag "{tag}".', ephemeral=True
                )

    @commands.slash_command(name="update", description="Updates an existing tag.")
    async def update(self, inter: disnake.ApplicationCommandInteraction):
        """
        Updates an existing tag.

        Parameters:
        - inter: The disnake.ApplicationCommandInteraction object representing the interaction.

        Returns:
        - None
        """
        await inter.response.send_modal(UpdateTagModal(server_id=str(inter.guild.id)))

    @commands.slash_command(
        name="reset", description="Resets the call counter for a tag."
    )
    async def reset(self, inter: disnake.ApplicationCommandInteraction, tag: str):
        """
        Resets the usage count of a tagged message in the database.

        Parameters:
        - inter: The interaction object representing the slash command interaction.
        - tag: The name of the tag to reset the call counter for.

        Returns:
        - None

        Raises:
        - None
        """
        server_id = str(inter.guild.id)

        if await tag_exists(server_id, tag):
            await reset_usage_count(server_id, tag)
            await inter.response.send_message(
                f'Call counter for tag "{tag}" reset.', ephemeral=True
            )
        else:
            await inter.response.send_message(
                f'No message found for tag "{tag}".', ephemeral=True
            )

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: disnake.Message):
        """
        Listens for messages starting with '%' and attempts to retrieve
        and display the corresponding tagged message.

        Parameters:
        - message (disnake.Message): The message object that triggered the event.

        Returns:
        - None

        Raises:
        - None
        """
        if message.author == self.bot.user or not message.content:
            return

        if find_tag_in_string(message.content):
            tag = find_tag_in_string(message.content)[0]
            if len(tag) < 3:
                return
            server_id = str(message.guild.id)

            tag_info = await get_message(server_id, tag)

            if tag_info:
                await increment_usage_count(server_id, tag)
                await message.channel.send(tag_info["content"])
            else:
                echo = await get_similar_tags(server_id, tag)
                if echo:
                    suggestions = [str(e[0]) for e in echo]
                    await message.channel.send(
                        f'No message found for tag "{tag}".'
                        + f"Suggestions: {', '.join(suggestions)}"
                    )
                else:
                    await message.channel.send(f'No message found for tag "{tag}".')


def setup(bot):
    """
    Adds the TagCommands cog to the bot.

    Parameters:
    - bot: The bot instance to add the cog to.
    """
    bot.add_cog(TagCommands(bot))

"""A module that contains the TagCommands class,
which is a Cog for handling commands related to tagging messages within Discord servers.

This module provides functionality to add, retrieve, update, delete,
and reset tagged messages in a database.

Classes:
- TagCommands:
A Cog for handling commands related to tagging messages within Discord servers.
"""

import datetime
import re

import disnake
from disnake.ext import commands

# Import functions from the database module to interact with tagged messages.
from db import (
    add_message,
    delete_message,
    get_all_messages,
    get_message,
    get_similar_tags,
    increment_usage_count,
    reset_usage_count,
    update_message,
)


class TagCommands(commands.Cog):
    """
    A Cog for handling commands related to tagging messages within Discord servers.
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

    @commands.slash_command(name="add", description="Adds a tagged message.")
    async def add(
        self, inter: disnake.ApplicationCommandInteraction, tag: str, message: str
    ):
        """
        Adds a tagged message to the database.

        Parameters:
        - inter: The interaction object representing the slash command interaction.
        - tag: The tag to be added.
        - message: The message to be associated with the tag.

        If the tag already exists, suggests alternative tags.
        """
        server_id = str(inter.guild.id)

        # Check if the tag already exists in the database.
        if await tag_exists(server_id, tag):
            # Generate and suggest alternative tags.
            recommendations = generate_recommendations(tag)
            recommendations_str = ", ".join(recommendations)
            await inter.response.send_message(
                f"This tag already exists. Suggestions: {recommendations_str}."
                + f"The message you wanted to add is ```{message}```",
                ephemeral=True,
            )
        else:
            # Insert the new tag and message into the database.
            await add_message(server_id, tag, message, str(inter.author.id))
            await inter.response.send_message(f'Tag "{tag}" added successfully.')

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
            # Suggest similar tags if the requested tag is not found.
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
        from the database for the server, including details such as
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

    @commands.slash_command(
        name="update", description="Updates the content of a tagged message."
    )
    async def update(
        self, inter: disnake.ApplicationCommandInteraction, tag: str, message: str
    ):
        """
        Updates the content of a tagged message in the database.

        Parameters:
        - inter: The interaction object representing the slash command interaction.
        - tag: The tag name to update.
        - message: The new content of the tagged message.

        Returns:
        None

        Raises:
        None
        """
        server_id = str(inter.guild.id)

        if await tag_exists(server_id, tag):
            await update_message(server_id, tag, message)
            await inter.response.send_message(f'Tag "{tag}" updated successfully.')
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
            server_id = str(message.guild.id)

            tag_info = await get_message(server_id, tag)

            if tag_info:

                member = message.guild.get_member(int(tag_info["created_by"]))
                username = member.display_name if member else "Unknown user"
                embed = build_embed(tag_info, username)

                await increment_usage_count(server_id, tag)
                await message.channel.send(embed=embed)
            else:
                echo = await get_similar_tags(server_id, tag)
                if echo:
                    suggestions = [str(e[0]) for e in echo]
                    await message.channel.send(
                        f'No message found for tag "{tag}".'
                        + f"Suggestions: {', '.join(suggestions)}",
                        ephemeral=True,
                    )
                else:
                    await message.channel.send(
                        f'No message found for tag "{tag}".', ephemeral=True
                    )


async def tag_exists(server_id, tag):
    """Checks if a tag already exists in the database.

    Args:
        server_id (int): The ID of the server where the tag is being checked.
        tag (str): The name of the tag being checked.

    Returns:
        bool: True if the tag exists in the database, False otherwise.
    """
    tag_info = await get_message(server_id, tag)
    return tag_info is not None


def generate_recommendations(tag):
    """
    Generates tag recommendations based on the original tag.

    Parameters:
    - tag (str): The original tag to generate recommendations for.

    Returns:
    - list: A list of tag recommendations, each formed by appending a number to the original tag.
    """
    return [f"{tag}-{i}" for i in range(1, 4)]


def find_tag_in_string(s):
    """
    Finds and returns tags within a string that start with '%'.

    Args:
        s (str): The input string to search for tags.

    Returns:
        list: A list of tags found in the input string.

    """
    tags = re.findall(r"%(\w+)", s)
    return tags


def setup(bot):
    """
    Adds the TagCommands cog to the bot.

    Parameters:
    - bot: The bot instance to add the cog to.
    """
    bot.add_cog(TagCommands(bot))


def build_embed(tag_info, username):
    """
    Builds an embed for a tagged message.

    Args:
        tag_info (dict): A dictionary containing information about the tag.
            It should have the following keys:
            - 'tag': The tag name.

            - 'content':
            The content of the tag.

            - 'created_at':
            The creation date and time of the tag in the format '%Y-%m-%d %H:%M:%S'.

            - 'usage_count': The number of times the tag has been used.

        username (str): The username of the user who created the tag.

    Returns:
        disnake.Embed: An embed object representing the tagged message.

    """
    created_at = datetime.datetime.strptime(tag_info["created_at"], "%Y-%m-%d %H:%M:%S")
    created_at_formatted = created_at.strftime("%d/%m/%Y at %H:%M")

    embed = disnake.Embed(title=f"Tag: {tag_info['tag']}", color=disnake.Color.blue())
    embed.add_field(name="Content", value=tag_info["content"], inline=False)
    embed.add_field(name="Created by", value=username, inline=True)
    embed.add_field(name="Added", value=created_at_formatted, inline=True)
    embed.add_field(
        name="Number of calls",
        value=str(tag_info["usage_count"]),
        inline=True,
    )
    return embed

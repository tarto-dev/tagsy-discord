# -*- coding: utf-8 -*-
"""This module contains helper functions for Tagsy."""

import datetime
import re

import disnake
from sentry_sdk import capture_exception

from db.sqlite_handler import get_message


def generate_recommendations(tag):
    """
    Generates tag recommendations based on the original tag.

    Parameters:
    - tag (str): The original tag to generate recommendations for.

    Returns:
    - list: A list of tag recommendations, each formed by appending a number to the original tag.
    """
    return [f"{tag}-{i}" for i in range(1, 4)]


async def tag_exists(server_id, tag):
    """
    Checks if a tag already exists in the database.

    Args:
    - server_id (int): The ID of the server where the tag is being checked.
    - tag (str): The name of the tag being checked.

    Returns:
    - bool: True if the tag exists in the database, False otherwise.
    """
    tag_info = await get_message(server_id, tag)
    return tag_info is not None


def create_selected_message_content(inter):
    """
    Creates a formatted message content with information about the selected message.

    Args:
        inter: The interaction object containing the selected message.

    Returns:
        str: The formatted message content.
    """
    selected_message_content = inter.target.content
    original_author = inter.target.author
    original_link = inter.target.jump_url
    original_date = inter.target.created_at.strftime("%Y-%m-%d %H:%M:%S")

    selected_message_content = (
        f"Original author: {original_author}\n"
        f"Original date: {original_date} [jump]({original_link}) \n\n"
        f"{selected_message_content}"
    )

    return selected_message_content


def sentry_capture(exception, server_id=0, user_id=0):
    """
    Captures an exception and sends it to Sentry.

    Args:
    - exception (Exception): The exception to capture.
    - server_id (int): The ID of the server where the exception occurred.
    - user_id (int): The ID of the user who triggered the exception.

    Returns:
    - None
    """
    capture_exception(exception, extra={"server_id": server_id, "user_id": user_id})


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


def find_tag_in_string(s):
    """
    Finds and returns tags within a string that start with '§'.

    Args:
        s (str): The input string to search for tags.

    Returns:
        list: A list of tags found in the input string.
    """
    tags = re.findall(r"§(\w+[-\w]*)", s)
    return tags


def find_old_tag_in_string(s):
    """
    Deprecated function to find old tags in a string.

    Finds and returns tags within a string that start with '%'.

    Args:
        s (str): The input string to search for tags.

    Returns:
        list: A list of tags found in the input string.
    """
    tags = re.findall(r"%(\w+[-\w]*)", s)
    return tags

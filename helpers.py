# -*- coding: utf-8 -*-
"""This module contains helper functions for the Tagsy project.

The functions in this module provide various utilities for working with tags in the Tagsy project.
"""

import datetime
import re

import disnake

from db import get_message


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
    tags = re.findall(r"%(\w+[-\w]*)", s)
    return tags


def build_embed(tag_info, username):
    """
    Builds an embed for a tagged message.

    Args:
        tag_info (dict): A dictionary containing information about the tag.
            It should have the following keys:
            - 'tag': The tag name.
            - 'content': The content of the tag.
            - 'created_at': The creation date and time of the tag in the format '%Y-%m-%d %H:%M:%S'.
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

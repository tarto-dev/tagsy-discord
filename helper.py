# -*- coding: utf-8 -*-
"""This module contains helper functions for Tagsy."""

from db import get_message


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

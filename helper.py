# -*- coding: utf-8 -*-
"""This module contains helper functions for Tagsy."""

from sentry_sdk import capture_exception

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

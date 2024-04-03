"""
This module provides functions for interacting with a SQLite
database using the aiosqlite library.
It includes functions for setting up the database, adding, retrieving,
deleting, updating, and resetting messages.

Functions:
- db_setup():
Sets up the database by creating the necessary tables.

- add_message(server_id, tag, content, created_by):
Adds a new message to the database.

- get_similar_tags(server_id, tag):
Retrieves tags similar to the given one from the database.

- get_message(server_id, tag):
Retrieves a specific message by tag from the database.

- delete_message(server_id, tag):
Deletes a message associated with a tag from the database.

- update_message(server_id, tag, content):
Updates the content of a message associated with a tag in the database.

- get_all_messages(server_id):
Retrieve all messages and their details from the database for a specific server.

- increment_usage_count(server_id, tag):
Increments the usage count for a specific tag.

- reset_usage_count(server_id, tag):
Resets the usage count for a specific tag to zero.
"""

import aiosqlite
from config import DATABASE_FILE

DB_PATH = DATABASE_FILE


async def db_setup():
    """Sets up the database by creating the necessary tables."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """CREATE TABLE IF NOT EXISTS messages (
                            id INTEGER PRIMARY KEY,
                            server_id TEXT NOT NULL,
                            tag TEXT NOT NULL,
                            content TEXT NOT NULL,
                            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                            created_by TEXT NOT NULL,
                            usage_count INTEGER DEFAULT 1,
                            UNIQUE(server_id, tag)
                        )"""
        )
        await db.commit()


async def add_message(server_id, tag, content, created_by):
    """Adds a new message to the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO messages (server_id, tag, content, created_by) VALUES (?, ?, ?, ?)",
            (server_id, tag, content, created_by),
        )
        await db.commit()


async def get_similar_tags(server_id, tag):
    """Retrieves tags similar to the given one from the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT tag FROM messages WHERE server_id = ? AND tag LIKE ?",
            (server_id, "%" + tag + "%"),
        )
        return await cursor.fetchall()


async def get_message(server_id, tag):
    """Retrieves a specific message by tag from the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT
                tag, content, created_by, created_at, usage_count
            FROM messages
            WHERE server_id = ? AND tag = ?""",
            (server_id, tag),
        )
        row = await cursor.fetchone()
        if row:
            return {
                "tag": row[0],
                "content": row[1],
                "created_by": row[2],
                "created_at": row[3],
                "usage_count": row[4],
            }


async def delete_message(server_id, tag):
    """Deletes a message associated with a tag from the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "DELETE FROM messages WHERE server_id = ? AND tag = ?", (server_id, tag)
        )
        await db.commit()


async def update_message(server_id, tag, content):
    """Updates the content of a message associated with a tag in the database."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE messages SET content = ? WHERE server_id = ? AND tag = ?",
            (content, server_id, tag),
        )
        await db.commit()


async def get_all_messages(server_id):
    """
    Retrieve all messages and their details (tag, content, created_by, created_at, usage_count)
    from the database for a specific server.

    Args:
      server_id (str): The ID of the server from which to retrieve all messages.

    Returns:
      A list of dictionaries, each containing details about a message.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT tag, content, created_by, created_at, usage_count
            FROM messages
            WHERE server_id = ?
            """,
            (server_id,),
        )
        rows = await cursor.fetchall()

        # Convert rows to a list of dictionaries for easier access in the calling function
        messages = [
            {
                "tag": row[0],
                "content": row[1],
                "created_by": row[2],
                "created_at": row[3],
                "usage_count": row[4],
            }
            for row in rows
        ]

        return messages


async def get_all_tags_for_all_servers():
    """
    Retrieve all tags and their details (tag, content, created_by, created_at, usage_count)
    from the database for all servers.

    Returns:
      A list of dictionaries, each containing details about a tag.
    """
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            """
            SELECT server_id, tag, content, created_by, created_at, usage_count
            FROM messages
            """
        )
        rows = await cursor.fetchall()

        # Convert rows to a list of dictionaries for easier access in the calling function
        tags = [
            {
                "server_id": row[0],
                "tag": row[1],
                "content": row[2],
                "created_by": row[3],
                "created_at": row[4],
                "usage_count": row[5],
            }
            for row in rows
        ]

        return tags


async def increment_usage_count(server_id, tag):
    """Increments the usage count for a specific tag."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE messages SET usage_count = usage_count + 1 WHERE server_id = ? AND tag = ?",
            (server_id, tag),
        )
        await db.commit()


async def reset_usage_count(server_id, tag):
    """Resets the usage count for a specific tag to zero."""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE messages SET usage_count = 1 WHERE server_id = ? AND tag = ?",
            (server_id, tag),
        )
        await db.commit()

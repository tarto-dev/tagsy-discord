# Tagsy Discord Bot

Tagsy is a Discord bot designed to enhance server interaction by allowing users to create, retrieve, and manage custom tags. Implemented using the disnake library, Tagsy supports various commands and context menus, making it a versatile tool for server moderation and community engagement.

Table of Contents
=================

- [Invite](#invite-tagsy-on-your-discord)
- [Features](#features)
- [Setup](#setup)
  - [Installation Steps](#installation-steps)
- [Usage](#usage)
- [Development and Contributing](#development-and-contributing)
- [License](#license)

## Invite Tagsy on your discord

[![image](https://github.com/tarto-dev/tagsy-discord/assets/1745200/7d305ecd-1edb-4bf9-9693-5afc7fd7e32e)](https://discord.com/oauth2/authorize?client_id=1224771846247809156&permissions=8&scope=bot)

## Features

- **Tag Management**: Users can add, update, delete, and retrieve tags, which are essentially key-value pairs, to store and share information quickly.
- **Development Tools**: Special commands for bot owners to manage the bot, including database operations and configuration variable dumps.
- **Customizable Command Prefix**: The bot's command prefix is customizable, allowing for easy integration into servers with existing bot ecosystems.
- **Slash Commands Support**: Tagsy utilizes slash commands for an intuitive user experience, ensuring commands are easily discoverable and usable.
- **Context Menus**: Integrates with Discord's context menus, providing a seamless user interface directly from messages.

![Animation](https://github.com/tarto-dev/tagsy-discord/assets/1745200/30b5e1a9-d962-4715-bb47-7d8a14ead778)

## Setup

To run Tagsy on your server, you need to have Python 3.8 or higher and the following dependencies:

- [disnake](https://docs.disnake.dev/en/stable/)
- [aiosqlite](https://aiosqlite.omnilib.dev/en/latest/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

### Installation Steps

1. Clone this repository to your local machine or server.
2. Install the required dependencies using pip:
```shell
   pip install -r requirements.txt
```

3. Create a `.env` file in the root directory of the project and add your Discord bot token and database path:

```shell
   DISCORD_TOKEN=your_token_here
   DB_PATH=path_to_your_database.db
```

4. Run the bot:

```shell
   python bot.py
```

## Usage

Once the bot is running and invited to your Discord server, you can start creating and managing tags. Here are some of the available commands:

- **/add [tag] [message]**: Adds a new tag.
- **/get [tag]**: Retrieves the message associated with a tag.
- **/update [tag] [new_message]**: Updates the message for an existing tag.
- **/remove [tag]**: Deletes a tag.
- **/getall**: Lists all tags available on the server.

For bot owners, additional development commands are available for direct interaction with the database and configuration variables.

## Development and Contributing

Interested in contributing? Great! Here's how you can set up the bot for development and submit your contributions.

We welcome contributions of all kinds from the community! Whether you're looking to add new features, fix bugs, improve documentation, or help with code reviews, there's always a way to contribute. Here are some ways you can get involved:

- **Open Issues**: If you encounter a bug or have a suggestion for a new feature, please [open an issue](https://github.com/tarto-dev/tagsy-discord/issues/new) in the repository. Provide as much detail as you can, including steps to reproduce any bugs.
- **Fix existing issues**: [Existing issues](https://github.com/tarto-dev/tagsy-discord/issues) exists to be fixed, heads to issues list, pick the one you want and start coding ! Some issues are opened for [newcomers and new developers](https://github.com/tarto-dev/tagsy-discord/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22).
- **Review Code**: Take a look at [pull requests submitted by others](https://github.com/tarto-dev/tagsy-discord/pulls) and provide feedback. Code reviews are not only helpful for ensuring quality and consistency but also a great way to learn from others.
- **Open Pull Requests**: Ready to contribute your changes? [Submit a pull request](https://github.com/tarto-dev/tagsy-discord/compare)! Make sure to describe your changes clearly and link to any relevant issues. Please also ensure your code follows the project's coding standards and passes all tests.


1. Fork the repository and clone your fork to your local machine.
2. Set up a virtual environment for Python to manage dependencies separately:

    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the development dependencies:

    pip install -r requirements.txt

4. Create a `.env` file in the root directory with the necessary configuration variables:

    ```
    DISCORD_TOKEN=<your_discord_bot_token>
    DB_PATH=database.db
    ```

5. You can obtain a Discord bot token by registering a new application in the Discord Developer Portal at [https://discord.com/developers/applications](https://discord.com/developers/applications). Navigate to the "Bot" tab and click on "Add Bot".

6. Make your changes. Feel free to add new features, fix bugs, or improve the code.
7. Test your changes thoroughly.
8. Commit your changes and push them to your fork.
9. Submit a pull request with a clear description of the changes you've made.

Please follow our [contribution guidelines](CONTRIBUTING.md)

## License

Tagsy is released under the MIT License. See the [LICENSE](LICENSE) file for more details.


## Acknowledgments

- Special thanks to [Disnake](https://disnake.readthedocs.io/) for the Discord library.

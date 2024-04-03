# Discord Tag Bot

A Discord bot designed to manage and recall tagged messages within servers. This bot allows users to add, retrieve, update, delete, and list tagged messages, providing an organized way to store and access information quickly.

Got troubles ? Feel free to reach me on Discord: @tarto

# Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Bot](#running-the-bot)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

[![image](https://github.com/tarto-dev/tagsy-discord/assets/1745200/7d305ecd-1edb-4bf9-9693-5afc7fd7e32e)](https://discord.com/oauth2/authorize?client_id=1224771846247809156&permissions=8&scope=bot)


## Features

- Tag Management: Easily add, update, and delete tags for messages.
- Quick Retrieval: Swiftly retrieve messages using their associated tags.
- Usage Tracking: Monitor how often tagged messages are accessed.
- Server-specific Tags: Ensures tags and messages are specific to each server, maintaining privacy and organization.

## Getting Started
### Prerequisites

- Python 3.8 or higher
- pip for installing Python packages

### Installation

1. Clone the repository
```bash
git clone https://github.com/tarto-dev/tagsy-discord.git
cd discord-tag-bot
```
2. Set up a virtual environment

  - On Windows:
```shell
python -m venv venv
venv\Scripts\activate
```
  - On macOS/Linux:
```shell
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages

`pip install -r requirements.txt`

4. Set up the environment variables

Create a `.env` file in the root directory and add your [Discord bot token](https://discord.com/developers/docs/quick-start/getting-started#step-1-creating-an-app):
```
DISCORD_TOKEN=your_discord_bot_token_here
DB_PATH=database.db
```

### Running the Bot
- Ensure your virtual environment is activated.
- To start the bot, run:
`python bot.py`

![image](https://github.com/tarto-dev/tagsy-discord/assets/1745200/252c516d-82de-45f5-a164-cceb023c9db3)

### Deploying the bot
The bot currently support fast deployment over [fly.io](https://fly.io)

## Usage
Once the bot is running and invited to a server, you can use the following slash commands:

- `/add <tag> <message>`: Adds a message with a specified tag.
- `/get <tag>`: Retrieves a message by its tag.
- `/update <tag> <new_message>`: Updates the message associated with a tag.
- `/remove <tag>`: Deletes a tagged message.
- `/getall`: Lists all tagged messages in the server.

## Contributing

Contributions are welcome! Please feel free to fork the repository and submit pull requests.

## License

Distributed under the MIT License. See LICENSE for more information.

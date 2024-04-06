# Contributing to Tagsy


## Table of Contents
- [We Love Your Input!](#we-love-your-input)
- [We Develop with Github](#we-develop-with-github)
- [Using Github Flow](#using-github-flow)
- [Contributions Under MIT Software License](#contributions-under-mit-software-license)
- [Reporting Bugs](#reporting-bugs)
- [Writing Bug Reports](#writing-bug-reports)
- [Coding Style](#coding-style)
  - [How to Apply Coding Styles](#how-to-apply-coding-styles)
- [Project Structure](#project-structure)
  - [Adding New Features or Commands](#adding-new-features-or-commands)
- [Pre-commit Hooks](#pre-commit-hooks)
  - [Setting Up Pre-commit](#setting-up-pre-commit)
  - [Hooks Used](#hooks-used)
- [GitHub Actions Workflows](#github-actions-workflows)
  - [Workflow Jobs](#workflow-jobs)
  - [Deployment](#deployment)
- [License](#license)
- [References](#references)

## We love your input!

We want to make contributing to this project as easy and transparent as possible, whether it's:
- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html), So All Code Changes Happen Through Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](https://github.com/tarto-dev/tagsy-discord/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/tarto-dev/tagsy-discord/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:
- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Use a Consistent Coding Style

### Coding Style

Our project enforces a consistent coding style to ensure the codebase remains clean, readable, and maintainable. We use several tools to help with this:

- **Black** for Python code formatting. Black makes code review faster by producing the smallest diffs possible.
- **isort** to sort imports alphabetically, and automatically separated into sections and by type. It ensures that the imports are visually distinct and grouped.
- **pydocstringformatter** to format docstrings to adhere to the project's documentation standards.
- **bandit** for Python security audit to keep our codebase secure.

#### How to Apply Coding Styles

Before submitting your pull request, please make sure your contributions adhere to these styles. Here's how you can do it:

1. Run isort to sort your imports:

   `isort .`

2. Use Black to format your Python files:

   `black --safe --quiet .`

3. Run pydocstringformatter to ensure your docstrings follow our conventions:

   `pydocstringformatter --max-summary-lines=2 --linewrap-full-docstring .`

4. Execute bandit to check for common security issues:

   `bandit -r -lll .`

You can manually run these commands, or set up pre-commit hooks as described in the pre-commit section to automatically apply these styles and checks before each commit.

Ensuring your code follows these guidelines will help make the review process faster and smoother for everyone involved.

### Project Structure

Understanding the project's structure is crucial for contributions. Here's a breakdown of the main directories and files in the Tagsy Discord Bot project:

- **`/commands`**: This directory contains all the command modules that the bot can execute. Each file represents a separate command group or a single command.

- **`/db`**: Includes files related to database setup, schemas, and migrations. It's where the logic for interacting with the database resides.

- **`/events`**: Houses event handlers for the bot. These scripts define actions the bot should take in response to specific events on Discord (e.g., a message being posted or a user joining a server).

- **`/helpers`**: Contains utility functions and helpers used across various parts of the project. These might include formatting functions, common checks, or any utility logic.

- **`/modals`**: This directory is for Discord modal interactions, handling user input from custom modal dialogs.

- **`/views`**: Includes files for Discord views, such as interactive message components like buttons and select menus.

- **`config.py`**: The main configuration file for the bot. It reads environment variables and sets up global configurations.

- **`bot.py`**: The entry point of the Discord bot application. It initializes the bot, loads extensions, and starts the bot's event loop.

- **`.env.example`**: An example `.env` file. Copy this to `.env` and fill in your values to configure the bot.

- **`requirements.txt`**: Lists all Python package dependencies. Install these with `pip` to set up your development environment.

#### Adding New Features or Commands

When adding a new feature or command:
- Place your command logic in the `/commands` directory. If it's a part of a new category, consider creating a subdirectory.
- For database interactions, add your logic to the `/db` directory and ensure any new schemas or migrations are properly handled.
- Utilize the `/helpers` directory for shared logic to keep your code DRY.
- If your feature involves new events, `/events` is where those handlers should go.
- Remember to update `config.py` if your feature requires new configuration variables.

Please keep your code consistent with the existing style and structure. Happy coding!

### Pre-commit Hooks

To ensure the quality and consistency of our code, we use pre-commit hooks. Before you make a commit, these hooks will automatically check your changes for common issues.

#### Setting Up Pre-commit

1. Install the pre-commit package if you haven't already:

```shell
   pip install pre-commit
```

2. From the root of your local repository, set up the pre-commit hooks:

```shell
   pre-commit install
```

3. Now, the pre-commit hooks will run automatically on every commit. If you want to manually run all pre-commit hooks on all files, you can do so with:

```shell
   pre-commit run --all-files
```

#### Hooks Used

Our project uses the following hooks:
- Trailing whitespace remover
- EOF fixer
- YAML checker
- TOML checker
- Large files checker
- Requirements.txt fixer
- Encoding pragma fixer
- CSpell for spell checking
- isort for Python import sorting
- black for Python code formatting
- pydocstringformatter for docstring formatting
- bandit for Python security audit

These hooks help maintain code quality and prevent common coding issues. Please make sure to install and run them before submitting any pull requests.

### GitHub Actions Workflows

Our project uses GitHub Actions for continuous integration and delivery. The workflows defined in build.yml perform tasks such as spell checking, linting with pylint, and deployment.

#### Workflow Jobs

- **Spellcheck**: Checks spelling across the project.
- **Pylint**: Lints Python files to identify coding errors.
- **Deploy**: Automatically deploys the latest version of the master branch.

Contributors should ensure their pull requests pass these checks. You can see the status of these checks in your pull request page on GitHub.

#### Deployment

The deploy job in our GitHub Actions workflow automatically deploys the application to production when changes are merged to the master branch. It uses Fly.io for deployment. Make sure any changes you make are safe to deploy and have been thoroughly tested.


## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## References

This document was adapted from the open-source contribution guidelines for [Facebook's Draft](https://github.com/facebook/draft-js/blob/master/CONTRIBUTING.md)

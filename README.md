# Discord-Bot

## Goal of Project
The purpose of this Discord bot is to give timely notifications to Students in the Lakehead CS 2021 Guild.

## How Can I Contribute?
Make a fork of the project and pick an issue to resolve, or open a new one outlining the feature or bug you are fixing. Make your modifications and then open a pull request so it can be added to the repo! Even if you are fixing a typo or changing the `README.md`, all contributions are welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details on contributions, setting up the bot in full, and pull request rules.

## How It Works
This project is programmed in Python 3 and uses the [discord.py](https://github.com/Rapptz/discord.py) API wrapper `Bot` class framework, a subclass of the `Client` class that is driven for commands alongside event handling.

The due dates for each week are read from a maintained Google Sheets file using the Google Cloud Platform's `Google Sheets API` and the `google-api-python-client` library.

### Dependencies
Discord-Bot uses several Python modules bundled with discord.py. You can choose to install all the required dependencies at once using `pip3 install -r requirements.txt`.

## Resources and API's
### Resource List
* [discord.py Bot Command Documentation](https://discordpy.readthedocs.io/en/stable/ext/commands/)
* [GitHub Crash Course](https://www.freecodecamp.org/news/git-and-github-crash-course/)
* [Git-Tower (Free Account for Students With Student Card)](https://www.git-tower.com/)
* [Discord Developer Hub](https://discord.com/developers/applications/)
* [Code a Discord Bot Follow-Along](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)
  
### API List
* [Google Sheets Python API](https://developers.google.com/sheets/api/quickstart/python)
* [Discord API](https://discordpy.readthedocs.io/en/stable/api.html)

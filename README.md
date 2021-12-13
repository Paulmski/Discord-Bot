# Discord-Bot

## Goal of Project
The purpose of this Discord bot is to give timely notifications to Students in the Lakehead CS 2021 Guild.

## How Can I Contribute?
Make a fork of the project, and pick an issue or open a new one outlining the feature or bug you are fixing. Make your modifications and then open a pull request so it can be added to the repo! Even if you are fixing a typo or changing the `README.md`, all contributions are welcome!

See [CONTRIBUTING.md](CONTRIBUTING.md) for more details on contributions and pull request rules.

## How It Works
This project uses the [discord.py](https://github.com/Rapptz/discord.py) API wrapper Bot class framework, a subclass of the Client class that is driven for commands rather than event handling.

You can run your own version of the bot from a repl.it project or from your local machine. Create the Discord Bot Account through your [Applications page](https://discord.com/developers/applications), create an OAuth2 URL (check off bot and desired permissions), and then use the generated URL to invite the bot to your test server.

You will also need the bot token, which can be generated from the Build-A-Bot menu under Bot. Create a file called `secrets.py` in the src folder and store the token as a String constant called `DISCORD_TOKEN`. When making commits, do not add this file.

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

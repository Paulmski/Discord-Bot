# Contribution Guidelines

## Welcome to Discord-Bot!
Thank you for your interest in contributing to the Lakehead CS 2021 Guild's Discord-Bot project!

We wish to see your contribution to this project, no matter your skill level! This document will help walk you through getting started, the rules for this repo, setting up the Discord bot on your own server, and how you can contribute from here on out.

## Table of Contents
* [Getting Started](#Getting-Started)
* [Rules](#Rules)
* [Testing the Bot](#Testing-the-Bot)
    * [Creating a Bot account](#Creating-A-Bot-Account)
    * [Letting the bot into your test server](#Letting-the-Bot-Into-Your-Test-Server)
    * [Setting up `.env`](#Setting-Up-`.env`-Fully)
    * [Setting up Google Sheets API](#Making-Contact-With-The-Google-Sheets-API)
* [List of Ways You Can Contribute](#List-of-Ways-You-Can-Contribute)

## Getting Started
If you haven't already, install [Git and Git Bash](https://git-scm.com/downloads), a code editor like [Visual Studio Code](https://code.visualstudio.com/), and [Git Tower](https://git-tower.com) onto your local machine.

Before getting started with Git, it's best to read up and learn the basic commands, workflow, conventions, and etiquette. These resources are great for starting off:

* [GitHub Crash Course](https://www.freecodecamp.org/news/git-and-github-crash-course/)
* [GitHub SSH Key Generation Tutorial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
* [Branch Naming Convention and Workflow](https://gist.github.com/digitaljhelms/4287848)
* [discord.py Programming Follow-Along](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)

Assuming you already know Python, you should also refer to the [discord.py documentation](https://discordpy.readthedocs.io/en/stable/ext/commands/) when debugging, refactoring, or programming.

## Rules
For this project, we are looking to uphold Git etiquette and good workflow.

1. Whenever you want to make changes to the project, please fork the project.

2. Make sure you work in the `develop` branch or new branch when making changes in your fork.
3. **Do not make pull requests to the `main` branch**.
4. Pull requests should always be for the `develop` branch.

Sometimes pull requests will be denied or revised. This is only the nature of the project; changes and optimizations need to be made before it can be incorporated into the main branch.

## Testing the Bot
You can run your own version of the bot from a repl.it project or from your local machine.

### Creating a Bot Account
Firstly, create a Discord Bot Account through your [Applications page](https://discord.com/developers/applications). Give it an appropriate name and description. 

### Letting the Bot Into Your Test Server
Once you have done that, make sure to create a OAuth2 URL to invite your bot to your test server.

Go to OAuth2 > URL Generator and select `bot` as the scope. You should then give the bot the appropriate server permissions. The URL to invite your bot a server _you_ own will be at the bottom of the page.

### Setting Up `.env` Fully
In order for the bot to actually work, you need to fill in a file called `.env` in your `src` folder, something that isn't done automatically.

#### Token Generation
You will also need the bot `TOKEN` to run the bot on your local machine/repl.it.

This can be generated from Build-A-Bot under the Bot menu.
Create your bot, give it a name, and click `Click to Reveal Token` to see your bot's token. 

Do not share this token with anyone or the public (think of it as an RSA private key). If it does get leaked, you can always regenerate a new token from the same menu. 

#### Token Association
Assign the token as a String to a constant called `DISCORD_TOKEN`. Example:
```python
DISCORD_TOKEN = "v3RyR3A!diSCorDt0k3n1d"
```
When you commit and push changes to your fork, do not add `.env`. Although `.gitignore` does this for you, do not forcibly add it anyways.

#### Linking the Spreadsheet
Find the spreadsheet's ID (before the `/view#gid=0` parameter in the URL), and assign it as a String to a constant called `SPREADSHEET_ID` in `.env`.

You will also need to specify the `RANGE_NAME`. In Google Sheets, several spreadsheets are split into "books", the names of which can be seen along the bottom.

Specify the current semester's book followed by the range of cells in which the Course Name, Due Date, Assignment Name, Days Remaining, and Notes are. 

Example:
```python
SPREADSHEET_ID = "t0t@llyr3@lspr3@dsh33t!d"
RANGE_NAME = "Winter Semester!F1:J"
```

#### Linking an Announcements Channel
You should also link the `#announcements` channel in the `.env` so the bot knows where to post daily.

The announcement ID can be found at the end of a Discord URL, or its ID can be copied from the channel name if you have Developer Mode turned on.

Example:

```python
ANNOUNCEMENTS_CHANNEL = "123456789123456789"
```

#### `.env` Full Example
Once you filled all your `.env` variables, your file should look like this:

```python
DISCORD_TOKEN = "v3RyR3A!diSCorDt0k3n1d"
SPREADSHEET_ID = "t0t@llyr3@lspr3@dsh33t!d"
RANGE_NAME = "Winter Semester!F1:J"
ANNOUNCEMENTS_CHANNEL = "123456789123456789"
```

### Making Contact With The Google Sheets API
Now, you need to set up an email account and enable the Google Sheets API through Google Cloud Platform.

#### Step 1: Sign Up
Sign up for an account through [Google Cloud](https://cloud.google.com/) and then navigate to [the Google Cloud Console](https://console.cloud.google.com/).

#### Step 2: Create a New Project
Create a new project from the top navigation bar's "Select a project", and give your project any name you like. Now, your project name should be displayed in the spot you clicked "Select a project".

#### Step 3: Creating an OAuth2 Client ID
Navigate from Hamburger Menu > APIs & Services > Credentials > Create Credentials > OAuth Client ID.

Set the application type to `Desktop app` and give it any name.

Now, from the Hamburger Menu, go to `Marketplace` and look up `Google Sheets API`. Enable the API on your account then go back to the `APIs & Services` section as before.

Finally, you can download the OAuth2 Client ID. Download the file to the root directory Discord-Bot, and make sure you name it `credentials.json` !

#### Step 4: Run the bot!
The bot now has everything it needs to run. Run it from your local machine or a repl.it project and test it on a server you own.

## List of Ways You Can Contribute
### Feature Requests or Bug Reports
Do you have an idea for a feature the Discord bot could use? See a bug that needs squashing? Go ahead and add it to the [Issues browser](https://github.com/Paulmski/Discord-Bot/issues).

If you are submitting a feature, title it using the convention `Feature request: Feature name` and describe what you would like the feature to do.

Should you report a bug, title it using the convention `Bug: Bug name` and describe how you encountered the bug.

### Cleaning Up Code, Refactoring
If you want to improve the project's code, make those changes in the `develop` branch or a new branch in your fork, and then make a pull request!

You can add or edit comments, clean up whitespace, and enforce conventions where fit.

### Bug Fixing
When you find and fix a bug in the code, commit and push those changes in your fork. Make sure to test the Bot's full functionality in your own environment before making a pull request to the original repo's `develop` branch.

### Adding a New Feature
If you programmed a new feature, make a pull request to push those changes into the original repo's `develop` branch.

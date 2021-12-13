# Contribution Guidelines

## Welcome to Discord-Bot!
Thank you for your interest in contributing to the Lakehead CS 2021 Guild's Discord-Bot project!

We wish to see your contribution to this project, no matter your skill level! This document will help walk you through getting started, the rules for this repo, setting up the Discord bot on your own server, and how you can contribute from here on out.

## Table of Contents
___
[Getting Started](#Getting-Started)

[Rules](#Rules)

[Testing the Bot](#Testing-the-Bot)

[Methods of Contribution](#List-of-Ways-You-Can-Contribute)


## Getting Started
___
If you haven't already, install [Git and Git Bash](https://git-scm.com/downloads), a code editor like [Visual Studio Code](https://code.visualstudio.com/), and [Git Tower](https://git-tower.com) onto your local machine.

Before getting started with Git, it's best to read up and learn the basic commands, workflow, conventions, and etiquette. These resources are great for starting off:

* [GitHub Crash Course](https://www.freecodecamp.org/news/git-and-github-crash-course/)
* [GitHub SSH Key Generation Tutorial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
* [Branch Naming Convention and Workflow](https://gist.github.com/digitaljhelms/4287848)
* [discord.py Programming Follow-Along](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)

Assuming you already know Python, you should also refer to the [discord.py documentation](https://discordpy.readthedocs.io/en/stable/ext/commands/) when debugging, refactoring, or programming.

## Rules
___
For this project, we are looking to uphold Git etiquette and good workflow.

1. Whenever you want to make changes to the project, please fork the project.

2. Make sure you work in the `develop` branch or new branch when making changes in your fork.
3. **Do not make pull requests to the `main` branch**.
4. Pull requests should always be for the `develop` branch.

Sometimes pull requests will be denied or revised. This is only the nature of the project; changes and optimizations need to be made before it can be incorporated into the main branch.

## Testing the Bot
___
You can run your own version of the bot from a repl.it project or from your local machine.

### Creating a Bot Account
Firstly, create a Discord Bot Account through your [Applications page](https://discord.com/developers/applications). Give it an appropriate name and description. 

### Letting the Bot Into Your Test Server
Once you have done that, make sure to create a OAuth2 URL to invite your bot to your test server.

Go to OAuth2 > URL Generator and select `bot` as the scope. You should then give the bot the appropriate server permissions. The URL to invite your bot a server _you_ own will be at the bottom of the page.

### Token Generation
You will also need the bot `TOKEN` to run the bot on your local machine/repl.it.

This can be generated from Build-A-Bot under the Bot menu.
Create your bot, give it a name, and click `Click to Reveal Token` to see your bot's token. 

Do not share this token with anyone or the public (think of it as an RSA private key). If it does get leaked, you can always regenerate a new token from the same menu. 

### Token Association
Create a file called `secrets.py` in the src folder and assign the token as a String to a constant called `DISCORD_TOKEN`.

When you commit and push changes to your fork, do not add `secrets.py`. Although `.gitignore` does this for you, do not forcibly add it anyways.

## List of Ways You Can Contribute
___
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

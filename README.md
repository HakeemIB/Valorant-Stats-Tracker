# Valorant Account and Rank Lookup

A Python CLI tool and Discord bot that fetches a Valorant player's account info, current and peak competitive rank, Rank Rating (RR), and calculates K/D, HS%, and win rate across recent matches using the HenrikDev API.

## Features
* **Account & Rank Lookup:** Fetches Riot ID (`Name#Tag`), account level, region, platforms, current rank, peak rank, and RR.
* **Match History Analytics:** Calculates K/D, Headshot Percentage (HS%), and Win Rate across up to 10 recent matches.
* **Game Mode Filtering:** Supports `competitive`, `unrated`, and `swiftplay` match lookups.
* **Discord Bot (`/stats`):** Slash command interface with dropdown selectors, User Install support (usable in DMs, group chats, and servers), and dynamic embed sidebar colors matched to the player's rank.
* Keeps API keys secure using environment variables

## How to run
1. Clone or download this repository.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root folder and add your HenrikDev API key:

    get API from: https://api.henrikdev.xyz/dashboard/api-keys
    Get a Discord bot token from: https://discord.com/developers/applications
   ```env
   VALORANT_API_KEY=your_api_key_here
   ```
4. Run the program:
   ```bash
   python main.py
   ```

   or For the Discord Bot
    ```bash
   python bot.py
   ```

## Example Output
```text
Enter player name: hak33m
Enter player tag: takt
Enter player region (e.g., na, eu, ap): eu
Enter player platform (e.g., pc, console): pc
Enter player mode (e.g., competitive, unrated, swiftplay): competitive
Player ID: Hak33m#TAKT
Player Level: 201
Player Region: eu
Player Platform: ['PC', 'CONSOLE']
Player Peak Rank: Platinum 1
Player Rank: Gold 1
Player RR: 0
Player K/D (Competitive - Last 10): 0.96
Player HS% (Competitive): 21.9%
Player Win Rate (Competitive): 70.0% (7/10)
```
## What i practised
Making authenticated REST API GET requests with custom Authorization headers

Parsing nested JSON dictionaries and lists in Python

Returning and indexing tuples from functions

Managing secret keys safely with python-dotenv and .gitignore

Building Discord slash commands (app_commands), deferred responses, and custom embeds with discord.py

## Updates
[x] Recent match history loop calculating average K/D, Headshot%, and Win Rate

[x] Added game mode filtering (competitive, unrated, swiftplay)

[x] Added a Discord bot with /stats slash command, User Install support, and rank-colored embeds
# Valorant Account and Rank Lookup

A command-line Python program that fetches a Valorant player's account info, competitive rank, PEAK Competitive Rank, and Rank Rating (RR)

## Features
* Player ID(Name#Tag)
* Account Level
* Region
* Fetches current competitive rank tier, peak competitive rank tier and RR from recent MMR history
* Keeps API keys secure using environment variables

## How to run
1. Clone or download this repository.
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root folder and add your HenrikDev API key:

    get API from: https://api.henrikdev.xyz/dashboard/api-keys
   ```env
   VALORANT_API_KEY= "your_api_key_here"
   ```
4. Run the program:
   ```bash
   python main.py
   ```

## Example Output
```text
Enter player name: Hak33m
Enter player tag: TAKT
Enter player region (e.g., na, eu, ap): eu
Enter player platform (e.g., pc, console): pc
Player ID: Hak33m#TAKT
Player Level: 201
Player Region: eu
Player Platform: ['pc']
Player Peak Rank: Platinum 1
Player Rank: Gold 1
Player RR: 0
```
## What i practised
Making authenticated REST API GET requests with custom Authorization headers
Parsing nested JSON dictionaries and lists in Python
Returning and indexing tuples from functions
Managing secret keys safely with python-dotenv and .gitignore

## Planned Updates
[x] Account profile and current rank/RR lookup

[ ] Recent match history loop and average K/D calculator

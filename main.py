import requests
import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

VALORANT_API_KEY = os.getenv("VALORANT_API_KEY")
ACC_BASE_URL = "https://api.henrikdev.xyz/valorant/v2/account"
MMR_BASE_URL = "https://api.henrikdev.xyz/valorant/v3/mmr"

def get_player(name, tag, region, platform):
    ACC_url = f"{ACC_BASE_URL}/{name}/{tag}"
    MMR_url = f"{MMR_BASE_URL}/{region}/{platform}/{name}/{tag}"

    headers = {"Authorization": VALORANT_API_KEY}
    Get_ACC = requests.get(ACC_url, headers=headers)
    Get_MMR = requests.get(MMR_url, headers=headers)
    
    if Get_ACC.status_code == 200 and Get_MMR.status_code == 200:
        Player_ACC = Get_ACC.json()
        Player_MMR = Get_MMR.json()
        return Player_ACC, Player_MMR
    else:
        print(f"Error: {Get_ACC.status_code} - {Get_ACC.text}")
        print(f"Error: {Get_MMR.status_code} - {Get_MMR.text}")
        return None

player_name = input("Enter player name: ")
player_tag = input("Enter player tag: ").upper()
player_region = input("Enter player region (e.g., na, eu, ap): ").lower()
player_platform = input("Enter player platform (e.g., pc, console): ").lower()

PLAYER = get_player(player_name, player_tag, player_region, player_platform)

if PLAYER:
    print(f"Player ID: {PLAYER[0]['data']['name']}#{PLAYER[0]['data']['tag']}")
    print(f"Player Level: {PLAYER[0]['data']['account_level']}")
    print(f"Player Region: {PLAYER[0]['data']['region']}")
    print(f"Player Platform: {PLAYER[0]['data']['platforms']}")
    print(f"Player Peak Rank: {PLAYER[1]['data']['peak']['tier']['name']}")
    print(f"Player Rank: {PLAYER[1]['data']['current']['tier']['name']}")
    print(f"Player RR: {PLAYER[1]['data']['current']['rr']}")
else:
    print("Failed to retrieve player data.")
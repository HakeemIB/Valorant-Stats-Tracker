import requests
import os
from dotenv import load_dotenv

# Load variables from the .env file into the environment
load_dotenv()

VALORANT_API_KEY = os.getenv("VALORANT_API_KEY")
ACC_BASE_URL = "https://api.henrikdev.xyz/valorant/v2/account"
MMR_BASE_URL = "https://api.henrikdev.xyz/valorant/v3/mmr"
MATCHES_BASE_URL = "https://api.henrikdev.xyz/valorant/v4/matches"

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

def get_match_stats(name, tag, region, platform, mode="competitive", size=20):
    url = f"{MATCHES_BASE_URL}/{region}/{platform}/{name}/{tag}?mode={mode}&size={size}"
    headers = {"Authorization": VALORANT_API_KEY}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Match Error: {response.status_code} - {response.text}")
        return None

    matches = response.json().get("data", [])
    if not matches:
        return None

    total_kills = 0
    total_deaths = 0
    total_hs = 0
    total_body = 0
    total_leg = 0
    total_wins = 0

    for match in matches:
        for player in match["players"]:
            if (
                player["name"].lower() == name.lower()
                and player["tag"].lower() == tag.lower()
            ):
                stats = player["stats"]
                total_kills += stats["kills"]
                total_deaths += stats["deaths"]
                total_hs += stats["headshots"]
                total_body += stats["bodyshots"]
                total_leg += stats["legshots"]

                player_team = player["team_id"].lower()
                for team in match["teams"]:
                    if team["team_id"].lower() == player_team and team["won"]:
                        total_wins += 1
                        break
                break

    total_shots = total_hs + total_body + total_leg
    matches_counted = len(matches)

    kd = round(total_kills / total_deaths, 2) if total_deaths > 0 else float(total_kills)
    hs_pct = round((total_hs / total_shots) * 100, 1) if total_shots > 0 else 0.0
    win_rate = round((total_wins / matches_counted) * 100, 1) if matches_counted > 0 else 0.0

    return {
        "kd": kd,
        "hs_pct": hs_pct,
        "win_rate": win_rate,
        "wins": total_wins,
        "matches_counted": matches_counted,
        "mode": mode,
    }

if __name__ == "__main__":
    player_name = input("Enter player name: ")
    player_tag = input("Enter player tag: ").upper()
    player_region = input("Enter player region (e.g., na, eu, ap): ").lower()
    player_platform = input("Enter player platform (e.g., pc, console): ").lower()
    player_mode = input("Enter player mode (e.g., competitive, unrated, swiftplay): ").lower()

    if player_mode not in ("competitive", "unrated", "swiftplay"):
        print("Invalid mode selected. Defaulting to competitive.")
        player_mode = "competitive"

    PLAYER = get_player(player_name, player_tag, player_region, player_platform)
    MATCH_STATS = get_match_stats(player_name, player_tag, player_region, player_platform, player_mode)

    if PLAYER:
        print(f"Player ID: {PLAYER[0]['data']['name']}#{PLAYER[0]['data']['tag']}")
        print(f"Player Level: {PLAYER[0]['data']['account_level']}")
        print(f"Player Region: {PLAYER[0]['data']['region']}")
        print(f"Player Platform: {PLAYER[0]['data']['platforms']}")
        print(f"Player Peak Rank: {PLAYER[1]['data']['peak']['tier']['name']}")
        print(f"Player Rank: {PLAYER[1]['data']['current']['tier']['name']}")
        print(f"Player RR: {PLAYER[1]['data']['current']['rr']}")

        if MATCH_STATS:
            mode_label = MATCH_STATS["mode"].capitalize()
            print(f"Player K/D ({mode_label} - Last {MATCH_STATS['matches_counted']}): {MATCH_STATS['kd']}")
            print(f"Player HS% ({mode_label}): {MATCH_STATS['hs_pct']}%")
            print(f"Player Win Rate ({mode_label}): {MATCH_STATS['win_rate']}% ({MATCH_STATS['wins']}/{MATCH_STATS['matches_counted']})")
        else:
            print(f"No recent {player_mode} matches found.")
    else:
        print("Failed to retrieve player data.")
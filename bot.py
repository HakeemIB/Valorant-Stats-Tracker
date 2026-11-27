import os
from typing import Literal
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from main import get_player, get_match_stats

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

RANK_COLORS = {
    "iron": 0x4F4F4F,
    "bronze": 0xA87143,
    "silver": 0xC0C6C9,
    "gold": 0xECC34B,
    "platinum": 0x45A8B8,
    "diamond": 0xD482E8,
    "ascendant": 0x32B86B,
    "immortal": 0xBA3654,
    "radiant": 0xFFFFAA,
    "unranked": 0x7F8C8D,
}


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Online as {bot.user} — Slash commands synced!")


@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@bot.tree.command(name="stats", description="Look up a Valorant player's rank and match stats")
@app_commands.describe(
    name="Riot ID name (e.g., Hak33m)",
    tag="Riot tag without # (e.g., TAKT)",
    region="Server region (defaults to eu)",
    platform="Gaming platform (defaults to pc)",
    mode="Match history game mode (defaults to competitive)",
)
async def stats(
    interaction: discord.Interaction,
    name: str,
    tag: str,
    region: Literal["eu", "na", "ap", "kr", "latam", "br"] = "eu",
    platform: Literal["pc", "console"] = "pc",
    mode: Literal["competitive", "unrated", "swiftplay"] = "competitive",
):
    await interaction.response.defer()

    player = get_player(name, tag.upper(), region, platform)
    match_stats = get_match_stats(name, tag.upper(), region, platform, mode=mode)

    if player:
        acc_data = player[0]["data"]
        mmr_data = player[1]["data"]

        player_id = f"{acc_data['name']}#{acc_data['tag']}"
        level = acc_data["account_level"]
        platforms = ", ".join(acc_data["platforms"])
        current_rank = mmr_data["current"]["tier"]["name"]
        peak_rank = mmr_data["peak"]["tier"]["name"]
        rr = mmr_data["current"]["rr"]

        rank_tier = current_rank.split()[0].lower() if current_rank else "unranked"
        embed_color = RANK_COLORS.get(rank_tier, 0xFF4655)

        embed = discord.Embed(
            title=player_id,
            description=f"Region: **{acc_data['region'].upper()}** | Platform: **{platforms}**",
            color=embed_color,
        )
        embed.add_field(name="Current Rank", value=current_rank, inline=True)
        embed.add_field(name="Rank Rating", value=f"{rr} RR", inline=True)
        embed.add_field(name="Peak Rank", value=peak_rank, inline=True)
        embed.add_field(name="Account Level", value=str(level), inline=True)

        if match_stats:
            mode_label = match_stats["mode"].capitalize()
            embed.add_field(
                name=f"K/D ({mode_label} • Last {match_stats['matches_counted']})",
                value=str(match_stats["kd"]),
                inline=True,
            )
            embed.add_field(
                name=f"HS% ({mode_label})",
                value=f"{match_stats['hs_pct']}%",
                inline=True,
            )
            embed.add_field(
                name=f"Win Rate ({mode_label})",
                value=f"{match_stats['win_rate']}% ({match_stats['wins']}/{match_stats['matches_counted']})",
                inline=True,
            )
        else:
            embed.add_field(
                name=f"{mode.capitalize()} Matches",
                value="No recent matches found for this mode/platform.",
                inline=False,
            )

        embed.set_footer(text="Valorant Stats Tracker • HenrikDev API")
        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send(
            f"Could not find **{name}#{tag.upper()}** in `{region.upper()}` (`{platform}`), or the API returned an error."
        )


bot.run(DISCORD_TOKEN)
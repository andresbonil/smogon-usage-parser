import discord
import json
import nodejs
import os

from discord.ext import commands
from discord import app_commands
import config

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("bot is running")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(description="shutdown")
async def shutdown(req):
    sent = False
    if req.user.id == config.owner_id:
        shutdown_embed = discord.Embed(
            title="Bot Update", description="Bot is now shutting down.", color=0x8EE6DD
        )
        await req.channel.send(embed=shutdown_embed)
        await bot.close()
    else:
        return


@bot.tree.command(description="test_data")
async def test_data(
    interaction: discord.interactions,
    pokemon: str,
):
    nodejs.call(
        [
            "dist/index.js",
            "-d",
            "2019-08",
            "-f",
            "gen7vgc2019ultraseries",
            "-r",
            "1760",
            "-o",
            "./",
        ]
    )
    try:
        file = open("2019-08/gen7vgc2019ultraseries-1760/usage.json", "r")
        stats = json.load(file)
        pokemonKey = {}
        for entry in stats:
            temp = {}
            for ability in entry["abilities"]:
                temp[ability["ability"]] = ability["percent"]
            entry["abilities"] = temp
            #print(temp)
            temp = {}
            for item in entry["items"]:
                temp[item["item"]] = item["percent"]
            entry["items"] = temp
            pokemonKey[entry["name"]] = {  
                "types": entry["types"], #list of 1 or 2
                "stats": entry["stats"], #dictionary with keys of hp, atk, def, spa, spd, spe
                "abilities": entry["abilities"], #list of dictionaries with ability and usage percent 
                "raw_count": entry["raw_count"], #int, possibly sample size? 
                "percent": entry["percent"], #overall usage percentage
                "ranking": entry["ranking"], #usage ranking
                "viability": entry["viability"], #letter grade ranking viability? not sure 
                "items": entry["items"], #dictionary with key of item name
                "spreads": entry["spreads"], #list of dictionaries with spreads, return top 3 
                "moves": entry["moves"] #dictioary with keys moves, type, and percent
    }
        
        await interaction.response.send_message(stats[pokemon])
    except:
        await interaction.response.send_message(f"Could not find stats or open file.")


@bot.tree.command(description="request_data")
async def request_data(
    interaction: discord.interactions,
    format: str,
    date: str,
    rating: str,
    pokemon: str,
):
    # await ctx.send("Args are {}, {}, {}, {}".format(format, date, rating))
    # nodejs.call(
    #     [
    #         "dist/index.js",
    #         "-d",
    #         date,
    #         "-f",
    #         format,
    #         "-r",
    #         rating,
    #         "-o",
    #         "./",
    #     ]
    # )
    try:
        stats = open("{}/{}-{}/usage.json".format(date, format, rating))
        stats = json.load(stats)
        await interaction.response.send_message(stats[pokemon])
    except:
        await interaction.response.send_message(f"Could not find stats or open file.")


@bot.tree.command(description="hello")
async def hello(interaction: discord.interactions):
    await interaction.response.send_message(f"Hey {interaction.user.mention}")


@bot.tree.command(description="say")
@app_commands.describe(thing_to_say="What should be said?")
async def say(interaction: discord.Interaction, thing_to_say: str):
    await interaction.response.send_message(
        f"{interaction.user.name} said `{thing_to_say}`"
    )


bot.run(config.token)

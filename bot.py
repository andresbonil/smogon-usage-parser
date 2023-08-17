import discord
import json
import nodejs
import os
import pypokedex
import requests

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
        await req.channel.respond(embed=shutdown_embed)
        await bot.close()
    else:
        return


@bot.tree.command(description="test_data")
async def test_data(req, pokemon: str):
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
            # print(temp)
            temp = {}
            for item in entry["items"]:
                temp[item["item"]] = item["percent"]
            entry["items"] = temp
            pokemonKey[entry["name"]] = {
                "types": entry["types"],  # list of 1 or 2
                "stats": entry[
                    "stats"
                ],  # dictionary with keys of hp, atk, def, spa, spd, spe
                "abilities": entry[
                    "abilities"
                ],  # list of dictionaries with ability and usage percent
                "raw_count": entry["raw_count"],  # int, possibly sample size?
                "percent": entry["percent"],  # overall usage percentage
                "ranking": entry["ranking"],  # usage ranking
                "viability": entry[
                    "viability"
                ],  # letter grade ranking viability? not sure
                "items": entry["items"],  # dictionary with key of item name
                "spreads": entry[
                    "spreads"
                ],  # list of dictionaries with spreads, return top 3
                "moves": entry["moves"],  # dictioary with keys moves, type, and percent
            }
        #print(pokemon)
        #print(pokemonKey[pokemon])
        if pokemon not in pokemonKey:
            await req.response.send_message(f"Pokemon is not in this dataset! Double check Pokemon name!")
            return
        else:
            try:
                url = "https://pokeapi.co/api/v2/pokemon/" + pokemon.lower()
                response = requests.get(url)
                response = response.json()
                embed = discord.Embed(title=pokemon, description="Pokemon Statistics")
                
                embed.set_thumbnail(url=response["sprites"]["front_default"])         
                types = pokemonKey[pokemon]["types"]
                # if len(types) > 1:
                #    
                # else:
                #     embed.add_field(name="Type", value="Type1: {}".format(types[0].capitalize()), inline=False) 
                typestr = ""
                if len(types) == 1:
                    typestr += types[0].capitalize()
                    embed.add_field(name="Type", value=typestr, inline=False)
                else:
                    typestr += types[0].capitalize() + ", " + types[1].capitalize()
                    embed.add_field(name="Types", value=typestr, inline=False)
                abilities = pokemonKey[pokemon]["abilities"]    
                abilitystr = ""
                for ability in abilities:
                    abilitystr += "{}: {}% Usage".format( ability, abilities[ability]) + "\n"
                embed.add_field(name="Ability Usage", value=abilitystr, inline =False)

                await req.channel.send(embed=embed)

                # e = discord.Embed(
                #     title="{} Type(s)".format(pokemon),
                #     description=pokemonKey[pokemon]["types"],
                # )
                # url = "https://pokeapi.co/api/v2/pokemon/" + pokemon.lower()
                # response = requests.get(url)
                # response = response.json()
                # e.set_thumbnail(url=response["sprites"]["front_default"])
                # # e.set_image(url=p.sprites["front_default"])
                # await req.channel.send(embed=e)
                # await interaction.response.send_message(pokemonKey[pokemon]["types"])
            except:
                await req.response.send_message(
                    f"Failed to create embed!"
                )
    except:
        await req.response.send_message(f"Could not find stats or open file.")


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

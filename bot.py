import discord
import json
import nodejs

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
async def test_data(req):
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
    return

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

import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot allumé !")

    await bot.load_extension("cogs.info")

    try:
        synced = await bot.tree.sync()
        print(f"Commandes slash synchro : {len(synced)}")
    except Exception as e:
        print(e)

bot.run(os.getenv('DISCORD_TOKEN'))
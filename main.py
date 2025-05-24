import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot allumé !")
    game = discord.Game("KOG - Community Gmod")
    await bot.change_presence(status=discord.Status.online, activity=game)

    try:
        synced = await bot.tree.sync()
        print(f"Commandes slash synchro : {len(synced)}")
    except Exception as e:
        print(e)

@bot.event
async def setup_hook():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(cog_name)
                print(f"Cog chargé : {cog_name}")
            except Exception as e:
                print(f"❌ Erreur lors du chargement de {cog_name} : {e}")

bot.run(os.getenv('DISCORD_TOKEN'))
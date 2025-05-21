import discord
from discord.ext import commands

import os
from dotenv import load_dotenv
load_dotenv()

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot allumé !")

    try:
        synced = await bot.tree.sync()
        print(f"Commandes slash synchro : {len(synced)}")
    except Exception as e:
        print(e)

@bot.tree.command(name="youtube", description="Affiche la chaine youtube de la KOG")
async def youtube(interaction: discord.Interaction):
    await interaction.response.send_message("Voici la chaine youtube de la KOG : ")

bot.run(os.getenv('DISCORD_TOKEN'))
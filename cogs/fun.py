import discord
import random
from discord import app_commands
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="roll", description=("Choisis un chiffre aléatoire entre 1 et 100"))
    async def roll(self, interaction: discord.Interaction):
        number = random.randint(0, 100)
        await interaction.response.send_message(f"🎲 Tu as tiré le chiffre : {number}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
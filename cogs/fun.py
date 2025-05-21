import discord
import random
from discord import app_commands
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="roll", description=("Choisis un chiffre aléatoire entre 1 et 100"))
    @app_commands.describe(
        min = "Valeur minimal",
        max = "Valeur maximal"
    )
    async def roll(self, interaction: discord.Interaction, min: int = 1, max: int = 100):

        if min >= max:
            await interaction.response.send_message("❌ La valeur minimal ne peut être supérieur ou égal à la valeur maximal", ephemeral=True)
            return

        number = random.randint(min, max)
        await interaction.response.send_message(f"🎲 Tu as tiré un nombre entre {min} et {max}, le résultat est : {number}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Fun(bot))
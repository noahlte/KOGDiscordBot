import discord
from discord import app_commands
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #Commande / pour afficher la chaine youtube de la KOG
    @app_commands.command(name="youtube", description="Affiche la chaine YouTube de la KOG")
    async def youtube(self, interaction: discord.Interaction):
        await interaction.response.send_message("📺 Voici la chaîne YouTube de la KOG : https://youtube.com/")
    
    #Commande / pour afficher le site internet de la KOG
    @app_commands.command(name="site", description="Affiche le site internet de la KOG")
    async def site(self, interaction: discord.Interaction):
        await interaction.response.send_message("Voici le site de la KOG : https://www.kog-community.com/")
    
    #Commande / pour afficher la boutique de la KOG
    @app_commands.command(name="boutique", description="Affiche la boutique de la KOG")
    async def boutique(self, interaction: discord.Interaction):
        await interaction.response.send_message("Voici la boutique de la KOG : https://www.kog-community.com/shop")
    
    #Commande / pour afficher le TOP SERVEUR
    @app_commands.command(name="vote", description="Affiche le TOP SERVEUR des serveurs KOG")
    async def vote(self, interaction: discord.Interaction):
        liste_serveur = [
            "Serveur SWTOR : https://top-serveurs.net/garrys-mod/kog-swtor"
            ]
        
        result = "\n".join(liste_serveur)
        await interaction.response.send_message(f"Vote pour la KOG :\n{result}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Info(bot))
import discord
from discord import app_commands
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="ban", description="Banni le joueur mentionné")
    @app_commands.describe(
        member = "Le membre à bannir",
        reason = "La raison du banissement"
    )
    async def ban(self, interaction : discord.Interaction, member: discord.Member, reason: str = "Aucune raison n'a été spécifié"):
        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ Tu n'as pas la permission de bannir.", ephemeral=True)
            return

        if member == interaction.guild.owner:
            await interaction.response.send_message("❌ Je ne peux pas bannir le propriétaire du serveur.", ephemeral=True)
            return

        if member.top_role.position >= interaction.guild.me.top_role.position:
            await interaction.response.send_message("❌ Mon rôle est trop bas pour bannir ce membre.", ephemeral=True)
            return
        
        await member.ban(reason=reason)
        await interaction.response.send_message(f"{member.mention} a été banni pour : **{reason}**")

    @app_commands.command(name="kick", description="Kick le joueur mentionné")
    @app_commands.describe(
        member = "Le membre à bannir",
        reason = "La raison du banissement"
    )
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "Aucune raison n'a été spécifié"):
        if not interaction.user.guild_permissions.kick_members:
            await interaction.response.send_message("❌ Tu n'as pas la permission de kick.", ephemeral=True)
            return
        
        if member == interaction.guild.owner:
            await interaction.response.send_message("❌ Je ne peux pas kick le propriétaire du serveur.", ephemeral=True)
            return

        if member.top_role.position >= interaction.guild.me.top_role.position:
            await interaction.response.send_message("❌ Mon rôle est trop bas pour kick ce membre.", ephemeral=True)
            return
        
        await member.kick(reason=reason)
        await interaction.response.send_message(f"{member.mention} a été kick pour : **{reason}**")

async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
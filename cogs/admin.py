import discord
from discord import app_commands
from discord.ext import commands
import asyncio

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

    @app_commands.command(name="mute", description="Mute le joueur mentionné")
    @app_commands.describe(
        member = "Le membre à bannir",
        duration = "Durée (Ex: 10s, 5m, 1h)",
        reason = "La raison du mute"
    )
    async def mute(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = "Aucune raison n'a été spécifié"):
        if not interaction.user.guild_permissions.moderate_members:
            await interaction.response.send_message("❌ Tu n'as pas la permission de mute.", ephemeral=True)
            return
        
        muted_role = discord.utils.get(interaction.guild.roles, name = "Muted")
        if not muted_role:
            await interaction.response.send_message("❌ Le rôle 'Muted' n'existe pas. Crée-le d'abord.", ephemeral=True)
            return
        
        time_in_seconds = self.parse_duration(duration)
        if time_in_seconds is None:
            await interaction.response.send_message("❌ Durée invalide. Utilise s (secondes), m (minutes), ou h (heures)", ephemeral=True)
            return
        
        await member.add_roles(muted_role, reason=reason)
        await interaction.response.send_message(f"🔇 {member.mention} a été mute pour {duration}. Raison : {reason}")

        await asyncio.sleep(time_in_seconds)
        await member.remove_roles(muted_role, reason="Fin du mute automatique")
        try:
            await member.send(f"✅ Tu as été démuté dans {interaction.guild.name}.")
        except:
            pass

    def parse_duration(self, duration_str: str) -> int | None:
        try:
            unit = duration_str[-1]
            value = int(duration_str[:-1])
            match unit:
                case "s": return value
                case "m": return value * 60
                case "h": return value * 3600
        except:
            return None


async def setup(bot: commands.Bot):
    await bot.add_cog(Admin(bot))
import discord
from discord import app_commands
from discord.ext import commands

from datetime import datetime

class Moderation(commands.Cog):

    # ───────────────────────────────────────────────
    # 📜 Moderation function
    # ───────────────────────────────────────────────

    def __init__(self, bot):
        self.bot = bot
    
    def build_moderation_embed(self, action: str, member_mention: str, staff_mention: str, reason: str, avatar_url: str, date: str):
        embed = discord.Embed(
            title=f"🔨 This user has been {action}",
            color=discord.Color.dark_red()
        )

        embed.add_field(name="🙍‍♂️Member :", value=member_mention, inline=True)
        embed.add_field(name="👮Staff :", value=staff_mention, inline=True)
        embed.add_field(name="📜Reason :", value=reason, inline=False)

        embed.set_thumbnail(url=avatar_url)
        embed.set_footer(text=f"{action.capitalize()} on {date}")
        return embed
    
    def get_log_setup(self, interaction):
        day_date = datetime.now().strftime("%m/%d/%y")
        setup_cog = self.bot.get_cog("Setup")
        log_channel_id = setup_cog.get_channel(interaction.guild.id, "log_channel")
        return day_date, log_channel_id
    
    def check_moderation_right(self, interaction, member, required_permission: str):

        bot_member = interaction.guild.me

        if not getattr(interaction.user.guild_permissions, required_permission):
            return "❌ You do not have the permission to do this"
        
        if not getattr(bot_member.guild_permissions, required_permission):
            return "❌ I (the bot) do not have the permission to do that."
        
        if member == interaction.guild.owner:
            return "❌ You do not have the permission to execute this command on the owner of the server"
        
        if member.top_role >= interaction.guild.me.top_role:
            return "❌ I do not have the permission to do this"

    
    async def log_and_respond(self, interaction, embed, log_channel_id, response_message: str):
        if log_channel_id:
            channel = interaction.guild.get_channel(log_channel_id)
            await interaction.response.defer(ephemeral=True)
            await interaction.followup.send(response_message)
            await channel.send(embed=embed)
        else:
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # ───────────────────────────────────────────────
    # 🛡️ BAN COMMANDS (/ban, /unban)
    # ───────────────────────────────────────────────

    @app_commands.command(name="ban", description="Ban the selected user")
    @app_commands.describe(
        member = "The user you want to ban",
        reason = "The reason why you want to ban the player"
    )
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason specified"):

        day_date, log_channel_id = self.get_log_setup(interaction)
        
        error = self.check_moderation_right(interaction, member, "ban_members")
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return

        embed = self.build_moderation_embed(
            action="banned",
            member_mention=member.mention,
            staff_mention=interaction.user.mention,
            reason=reason,
            avatar_url=member.display_avatar.url,
            date=day_date
        )

        await member.ban(reason=reason)

        await self.log_and_respond(interaction, embed=embed, log_channel_id=log_channel_id, response_message=f"The user {member.mention} has been banned")

    @app_commands.command(name="unban", description="Unban the user with his user id")
    @app_commands.describe(
        user_id = "The ID of the player you want to unban",
        reason="The reason why you want to unban the player"
    )
    async def unban(self, interaction: discord.Interaction, user_id: str, reason: str = "No reason specified"):

        day_date, log_channel_id = self.get_log_setup(interaction)

        if not interaction.user.guild_permissions.ban_members:
            await interaction.response.send_message("❌ You do not have the permission to unban someone", ephemeral=True)
            return
        
        try:
            user_id = int(user_id)
        except ValueError:
            await interaction.response.send_message("❌ The ID entered is invalid.", ephemeral=True)
            return
            
        ban_entries = [entry async for entry in interaction.guild.bans()]
        target_user = None
        for entry in ban_entries:
            if entry.user.id == user_id:
                target_user = entry.user
                break

        if target_user == None:
            await interaction.response.send_message("❌ This user is not banned", ephemeral=True)
            return
            
        await interaction.guild.unban(target_user)

        embed = self.build_moderation_embed(
            action="unbanned",
            member_mention=f"<@{user_id}>",
            staff_mention=interaction.user.mention,
            reason=reason,
            avatar_url=target_user.display_avatar.url,
            date=day_date
        )

        await self.log_and_respond(interaction, embed=embed, log_channel_id=log_channel_id, response_message=f"The user <@{user_id}> has been unbanned")
    
    # ───────────────────────────────────────────────
    # 🔨 KICK COMMANDS (/kick)
    # ───────────────────────────────────────────────


    @app_commands.command(name="kick", description="Kick the selected user off the server")
    @app_commands.describe(
        member = "Who you want to kick",
        reason = "The reason why you want to kick this user"
    )
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = "No reason specified"):

        day_date, log_channel_id = self.get_log_setup(interaction)

        error = self.check_moderation_right(interaction, member, "kick_members")
        if error:
            await interaction.response.send_message(error, ephemeral=True)
            return
        
        await member.kick(reason=reason)
        
        embed = self.build_moderation_embed(
            action="kicked",
            member_mention=member.mention,
            staff_mention=interaction.user.mention,
            reason=reason,
            avatar_url=member.display_avatar.url,
            date=day_date
        )

        await self.log_and_respond(interaction, embed=embed, log_channel_id=log_channel_id, response_message=f"The user {member.mention} has been kicked")

async def setup(bot):
    await bot.add_cog(Moderation(bot))


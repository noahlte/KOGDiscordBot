import discord
from discord import app_commands
from discord.ext import commands

import json
import os

CONFIG_PATH = "data/server_config.json"

class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()
    
    def load_config(self):
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r', encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    print(f"[⚠️] Le fichier {CONFIG_PATH} est vide ou corrompu. Réinitialisation.")
                    return {}
        return {}
    
    def save_config(self):
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)
    
    def set_channel(self, guild_id, key, channel_id):
        gid = str(guild_id)
        if gid not in self.config:
            self.config[gid] = {}
        self.config[gid][key] = channel_id
        self.save_config()

    def get_channel(self, guild_id, key):
        return self.config.get(str(guild_id), {}).get(key)

    @app_commands.command(name="setup-logs", description="Define the logs channel for this server")
    async def setup_logs(self, interaction: discord.Interaction, channel: discord.TextChannel):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You do not have the permission to use this command.", ephemeral=True)
            return
        
        self.set_channel(interaction.guild.id, "log_channel", channel.id)
        await interaction.response.send_message(f"✅ Logs channel define on {channel.mention}", ephemeral=True)
    
async def setup(bot):
    await bot.add_cog(Setup(bot))
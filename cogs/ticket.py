import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

class TicketView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="📩 Ouvrir un ticket", style=discord.ButtonStyle.green, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: Button):
        guild = interaction.guild
        category = discord.utils.get(guild.categories, name = "Tickets")

        existing = discord.utils.get(guild.text_channels, name=f"ticket-{interaction.user.id}")
        if existing:
            await interaction.response.send_message("❗ Tu as déjà un ticket ouvert.", ephemeral=True)
            return
        
        staff_role = discord.utils.get(guild.roles, name="Staff")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages = False),
            interaction.user: discord.PermissionOverwrite(read_messages = True, send_messages = True),
            guild.me: discord.PermissionOverwrite(read_messages = True)
        }

        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)

        channel = await guild.create_text_channel(
            name = f'ticket-{interaction.user.id}',
            category=category,
            overwrites=overwrites,
            topic=f"Ticket de {interaction.user.display_name}"
        )

        await channel.send(f'{interaction.user.mention}, un membre du staff va bientôt te répondre.')
        await interaction.response.send_message(f"✅ Ticket créé : {channel.mention}", ephemeral=True)

class Ticket(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setticket(self, ctx):
        view = TicketView()
        await ctx.send("Clique sur le bouton pour ouvrir un ticket :", view=view)
    
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def close(self, ctx):
        """Ferme un salon de ticket (doit être utilisé dans un salon nommé 'ticket-xxx')"""
        if not ctx.channel.name.startswith("ticket-"):
            await ctx.send("❌ Cette commande ne peut être utilisée que dans un salon de ticket.")
            return

        await ctx.send("🔒 Fermeture du ticket dans 5 secondes...")
        await asyncio.sleep(5)
        await ctx.channel.delete()

async def setup(bot: commands.Bot):
    await bot.add_cog(Ticket(bot))
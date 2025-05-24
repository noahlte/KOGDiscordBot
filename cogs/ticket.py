import discord
import asyncio
from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button

class ticket_launcher(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    @discord.ui.button(label="📩 Créer un ticket", style=discord.ButtonStyle.blurple, custom_id= "ticket_button")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        ticket = discord.utils.get(interaction.guild.text_channels, name=f"ticket-for-{interaction.user.name}-{interaction.user.discriminator}")
        if ticket is not None: await interaction.response.send_message(f"❌ Tu as déjà un ticket d'ouvert à {ticket.mention} !", ephemeral=True)
        else:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
                interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True),
                interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
            }
            channel = await interaction.guild.create_text_channel(name=f"ticket-for-{interaction.user.name}-{interaction.user.discriminator}", overwrites=overwrites, reason=f"Ticket for {interaction.user}")
            await channel.send(f"📩 {interaction.user.mention} à créer un ticket ! Un membre du staff arrivera dès que possible pour le prendre en charge.", view=main())
            await interaction.response.send_message(f"J'ai ouvert un tikcet pour toi : {channel.mention} !", ephemeral=True)

class confirm(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    @discord.ui.button(label= "Confirmer", style= discord.ButtonStyle.red, custom_id= "confirm")
    async def confirm_button(self, interaction: discord.Interaction, button: discord.Button):
        try:
            await interaction.channel.delete()
        except:
            await interaction.response.send_message("Erreur lors de la suppression du channel ! Soyez sûr que je possède la permission 'manage_channels'", ephemeral=True)

class main(discord.ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Fermer le ticket", style=discord.ButtonStyle.red, custom_id= "close")
    async def close(self, interaction: discord.Interaction, button: discord.Button):
        embed = discord.Embed(title="Êtes-vous sûr de vouloir fermer ce ticket ?", color= discord.Color.blurple())
        await interaction.response.send_message(embed=embed, view=confirm(), ephemeral=True)

class Ticket(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.added = False
        self.ticket_mod = 1374790363730018354
    
    @commands.Cog.listener()
    async def on_ready(self):
        if not self.added:
            self.bot.add_view(ticket_launcher())
            self.bot.add_view(main())
            self.added = True
    
    @app_commands.command(name="ticket", description="Lance le système de ticket")
    async def ticket(self, interaction: discord.Interaction):

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(f"❌ {interaction.user.mention}, tu n'as pas l'autorisation d'initialiser le système de ticket !")
            return

        embed = discord.Embed(title="Si tu as besoins de support, clique sur le bouton ci-dessous!", color=discord.Color.blue())
        await interaction.channel.send(embed=embed, view=ticket_launcher())
        await interaction.response.send_message("Le système de ticket à été mis en place", ephemeral=True)
    
    @app_commands.command(name="close", description="Ferme le ticket")
    async def close(self, interaction: discord.Interaction):
        if "ticket-for" in interaction.channel.name:
            embed = discord.Embed(title="Êtes-vous sûr de vouloir fermer ce ticket ?", color= discord.Color.blurple())
            await interaction.response.send_message(embed=embed, view=confirm(), ephemeral=True)
        else:
            await interaction.response.send_message("Ce channel n'est pas un ticket !", ephemeral=True)
    
    @app_commands.command(name="add-user", description="Ajoute un utilisateur au ticket !")
    @app_commands.describe(
        member = "L'utilisateur que tu veux ajouter au ticket"
    )
    async def add_user(self, interaction: discord.Interaction, member: discord.Member):
        if not interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("❌ Tu n'as pas la permission d'ajouter un utilisateur au channel !", ephemeral=True)
        
        if "ticket-for" in interaction.channel.name:
            await interaction.channel.set_permissions(member, view_channel = True, send_messages = True, attach_files = True, embed_links = True)
            await interaction.response.send_message(f"{member.mention} a été ajouté au ticket par {interaction.user.mention}")
        else:
            await interaction.response.send_message("Ce channel n'est pas un ticket !", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Ticket(bot))
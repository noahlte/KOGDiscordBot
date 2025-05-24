import discord
from discord import app_commands
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

async def generate_welcome_image(member: discord.Member) -> discord.File:
    background = Image.open("assets/background.png").convert("RGBA")

    avatar_url = member.display_avatar.replace(format="png", size=256).url
    response = requests.get(avatar_url)
    avatar_raw = Image.open(BytesIO(response.content)).resize((256, 256)).convert("RGBA")

    mask = Image.new("L", (256, 256), 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, 256, 256), fill=255)

    avatar_circle = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    avatar_circle.paste(avatar_raw, (0, 0), mask=mask)

    border_size = 256
    halo_padding = 8
    halo_size = border_size + 2 * halo_padding

    border = Image.new("RGBA", (halo_size, halo_size), (0, 0, 0, 0))
    border_draw = ImageDraw.Draw(border)
    border_draw.ellipse((0, 0, halo_size, halo_size), fill=(255, 255, 255, 255))
    border_draw.ellipse((halo_padding, halo_padding, halo_size - halo_padding, 239), fill=(0, 0, 0, 0))  # trou intérieur
    background.paste(border, (52, 14), border)

    background.paste(avatar_circle, (60, 22), avatar_circle)

    draw = ImageDraw.Draw(background)
    try:
        font = ImageFont.truetype("assets/fonts/DejaVuSans-Bold.ttf", 38)
    except:
        font = ImageFont.load_default()
    
    # Zone d'écriture (ajuste selon ton fond)
    text_x = 388
    text_top = 90     # Limite supérieure
    text_bottom = 200  # Limite inférieure

    # Texte multiligne à afficher
    lines = [f"BIENVENUE", "sur le serveur", member.guild.name]

    # Calcule la hauteur totale du bloc de texte
    line_spacing = 12  # espace entre lignes
    line_height = font.getbbox("Hg")[3]  # hauteur approx. d'une ligne
    total_height = len(lines) * line_height + (len(lines) - 1) * line_spacing

    # Position Y de départ pour centrer verticalement
    start_y = text_top + (text_bottom - text_top - total_height) // 2

    # Affiche chaque ligne avec espacement vertical
    for i, line in enumerate(lines):
        draw.text((text_x, start_y + i * (line_height + line_spacing)), line, font=font, fill=(255, 255, 255))


    buffer = BytesIO()
    background.save(buffer, format="PNG")
    buffer.seek(0)

    return discord.File(fp=buffer, filename="welcome.png")

class Arrive(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_log_channel(self, guild: discord.Guild):
        setup_cog = self.bot.get_cog("Setup")
        if setup_cog is None:
            return None
        return setup_cog.get_channel(guild.id, "arrive_channel")

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        log_channel_id = self.get_log_channel(member.guild)
        file = await generate_welcome_image(member)

        embed = discord.Embed(
            title="**__🎉 On a un nouveau membre sur le serveur !__**",
            description=f"Bienvenue {member.mention} sur le serveur **{member.guild.name}** 🎉",
            color=discord.Color.dark_purple()
        )
        embed.set_image(url="attachment://welcome.png")
        embed.set_footer(text="Nous sommes maintenant " + str(len(member.guild.members)) + " membres sur le serveur !")

        if log_channel_id:
            channel = member.guild.get_channel(log_channel_id)
            if channel:
                await channel.send(embed=embed, file=file)
            else:
                print(f"[⚠️] Salon introuvable avec l'ID {log_channel_id}")
        else:
            print("[⚠️] Aucun salon de log défini pour ce serveur.")

async def setup(bot: commands.Bot):
    await bot.add_cog(Arrive(bot))
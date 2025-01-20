#En este comando se desplegará un embed con toda la información posible de un usuario:

import discord
import discord
from datetime import datetime


async def quienes(interaction: discord.Interaction, member: discord.Member):
    try:
        discord_embed = discord.Embed(
            title=f"Info de {member}",
            color=discord.Color.blue(),
            type="rich",
            timestamp=datetime.now(),
            description=f"**🫅🏼 Nombre:** {member.name}\n\n**🆔 ID:** {member.id}\n\n**👁️ Estado:** {member.desktop_status}\n\n**📈 Actividad:** {member.activity.name if member.activity else 'N/A'}\n\n**📈 Rol más alto:** {member.top_role.mention}\n\n**😶‍🌫️ Fecha de creación de la cuenta:** {member.created_at}\n\n**🎯 Fecha de ingreso al servidor:** {member.joined_at}\n"
        )
    except Exception as e:
        print(f"No se pudo crear el embed por la siguiente razón: {e}")

    discord_embed.set_thumbnail(url=member.avatar.url if member.avatar else None)
    if member.banner:
        discord_embed.set_image(url=member.banner.url)

    try:
        await interaction.response.send_message(embed=discord_embed)
    except Exception as e:
        print(f"No se pudo enviar el mensaje por la siguiente razón: {e}")
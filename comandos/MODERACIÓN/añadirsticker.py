import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta

async def AñadirSticker(interaction: discord.Interaction, nombre_sticker: str, descripcion_sticker: str, archivo: discord.Attachment):
    try:
        # Descargar el archivo adjunto
        file = await archivo.to_file()
        discord_file = discord.File(file.fp, filename=file.filename)
        
        # Crear el sticker en el servidor
        await interaction.guild.create_sticker(name=nombre_sticker, description=descripcion_sticker, file=discord_file, emoji="🙂")

        # Enviar un mensaje de confirmación
        embed = discord.Embed(
            title="📝 **Añadir sticker**",
            description=f'Se ha añadido el sticker {nombre_sticker} correctamente',
            color=discord.Color.green()
        )
        embed.set_image(url=f"attachment://{archivo.filename}")
        await interaction.response.send_message(embed=embed, file=discord_file)
    except Exception as e:
        embed = discord.Embed(
            title="⚠️ **Error**",
            description=f'No se ha podido añadir el sticker {nombre_sticker} por {e}',
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
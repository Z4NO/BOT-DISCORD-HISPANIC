#En esta clase se listan las acciones que puede ha realizado un moderador en un servidor en concreto , buscaremos en la base de datos todas las acciones que ha realizado un moderador por su id 

import discord
from discord.ext import commands
import sqlite3

async def ListarAccionesModerador(interaction: discord.Interaction, cursor: sqlite3.Cursor , miembro: discord.Member):
    try:
        # Comprobamos si el usuario es owner y si está en la base de datos
        cursor.execute("SELECT * FROM owners WHERE idDiscord = ? AND SERVER_idSERVER = ?", (interaction.user.id, interaction.guild.id))
        row = cursor.fetchone()
        if row is None or interaction.user.id != interaction.guild.owner_id:
            embed = discord.Embed(
                title="🚫 **Permiso denegado**",
                description=f'No tienes permisos para usar este comando {interaction.user.mention}',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        # Obtenemos todas las acciones realizadas por el moderador
        cursor.execute("SELECT * FROM moderatoractions WHERE idModerador = ? AND idSERVER = ?", (miembro.id, miembro.guild.id,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            embed = discord.Embed(
                title="📋 **Acciones del moderador**",
                description=f'{miembro.name} no ha realizado ninguna acción como moderador',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        # Creamos un mensaje con todas las acciones realizadas por el moderador
        embed = discord.Embed(
            title="📋 **Acciones del moderador**",
            description=f'Acciones realizadas por {miembro.mention}',
            color=discord.Color.green()
        )
        for row in rows:
            embed.add_field(
                name=f'🔨 **{row[2]}** hacia: {row[3]}',
                value=f'📅 **Realizado el:** {row[5]}\n\n⏰ **Termina el:** {row[6]}\n\n📝 **Con el motivo:** {row[7]}',
                inline=False
            )
            
        embed.set_image(url=miembro.avatar.url)
        embed.set_footer(text=f'ID de la acción: {row[1]}')
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title="⚠️ **Error**",
            description=f'No se ha podido listar las acciones del moderador por {e}',
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
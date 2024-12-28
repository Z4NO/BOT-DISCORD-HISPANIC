#en este comando se verá la configuración guardada para cada servidor , se mostrará el prefijo , el canal de logs , el rol de cuarentena y el canal de moderación

import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta

async def VerConfig(interaction: discord.Interaction, cursor: sqlite3.Cursor):
    try:
        # Comprobamos si el usuario es owner y si está en la base de datos
        cursor.execute("SELECT * FROM owners WHERE idDiscord = ? AND SERVER_idSERVER = ?", (interaction.user.id, interaction.guild.id))
        row = cursor.fetchone()
        if row is None or interaction.user.id != interaction.guild.owner_id:
            embed = discord.Embed(title="Permiso denegado", description=f'No tienes permisos para usar este comando {interaction.user.mention}', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return

        # Obtenemos la configuración del servidor
        cursor.execute("SELECT * FROM server_configuration WHERE idSERVER = ?", (interaction.guild.id,))
        row = cursor.fetchone()
        if row is None:
            embed = discord.Embed(title="Configuración del servidor", description=f'No hay configuración para este servidor', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return

        # Creamos un mensaje con la configuración del servidor
        embed = discord.Embed(title="Configuración del servidor", description=f'Configuración del servidor **{interaction.guild.name}**', color=discord.Color.green())
        embed.add_field(name="Prefijo", value=row[3], inline=False)
        canal = interaction.guild.get_channel(row[2])
        embed.add_field(name="Canal de logs", value=canal.mention if canal is not None else "No establecido", inline=False)
        rol = interaction.guild.get_role(row[4])
        embed.add_field(name="Rol de cuarentena", value=rol.mention if rol is not None else "No establecido", inline=False)
        canal = interaction.guild.get_channel(row[5])
        embed.add_field(name="Canal de moderación", value=canal.mention if canal is not None else "No establecido", inline=False)
        automoderacion = row[6]
        embed.add_field(name="Automoderación", value="Activada" if automoderacion == 1 else "Desactivada", inline=False)
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        embed = discord.Embed(title="Error", description=f'No se ha podido obtener la configuración del servidor por {e}', color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
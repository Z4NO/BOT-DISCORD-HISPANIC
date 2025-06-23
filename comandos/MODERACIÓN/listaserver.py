import discord
from discord.ext import commands
import time
import sqlite3


#EN ESTA FUNCIÓN SE LISTAN LOS SERVIDORES EN LOS QUE ESTÁ EL BOT PERO LOS OBTENIDOS EN LA BASE DE  DATOS SQLLITE 
async def ListarServerEnDb(interaction: discord.Interaction, cursor: sqlite3.Cursor):
    try:
        #VAMOS A HACER QUE SOLO UN USUAIRO PUEDA LLAMAR A ESTE COMANDo
        if interaction.user.id != 751435990664478837:
            await interaction.response.send_message(f'No tienes permisos para usar este comando {interaction.user.mention}')
            return

        #OBTENEMOS LOS SERVIDORES DE LA BASE DE DATOS  
        cursor.execute("SELECT serverName FROM SERVER")
        servidores = cursor.fetchall()
        
        # Creamos un embed para mostrar la lista de servidores
        embed = discord.Embed(title="Lista de Servidores", color=discord.Color.blue())
        
        # Añadimos los servidores al embed
        for server in servidores:
            embed.add_field(name="Servidor", value=f'{server[0]} ', inline=False)
        
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        await interaction.response.send_message(f'No se ha podido mostrar los servidores por {e}')
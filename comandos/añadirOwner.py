import discord
from discord.ext import commands
import sqlite3

# EN ESTA FUNCIÓN EL CREADOR DE CADA GUILD PODRÁ AÑADIR UN OWNER/MODERADOR A SU SERVIDOR
async def AñadirOwner(interaction: discord.Interaction, member: discord.Member, cursor: sqlite3.Cursor, conn: sqlite3.Connection):   
    try:
        if interaction.user.guild.owner_id != interaction.user.id:
            embed = discord.Embed(
                title="Permiso Denegado",
                description=f'No tienes permisos para usar este comando {interaction.user.mention}',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return 
        # añadimos el miembro como owner en la base de datos
        cursor.execute("INSERT INTO owners (idOwners, ownerName, idDiscord, SERVER_idSERVER) VALUES (?, ?, ?, ?)", (member.id, member.name, member.id, interaction.guild.id))
        conn.commit()
        embed = discord.Embed(
            title="Owner Añadido",
            description=f'{member.mention} ha sido añadido como owner',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="Error",
            description=f'No se ha podido añadir a {member.mention} como owner por {e}',
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

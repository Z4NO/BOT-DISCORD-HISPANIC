#este comando listara en un embed a todos los owners del servidor
import discord
from discord.ext import commands
import sqlite3


async def listarOwner(interaction: discord.Interaction, cursor: sqlite3.Cursor):
    try:
        cursor.execute("SELECT ownerName,idDiscord FROM owners WHERE SERVER_idSERVER = ?", (interaction.guild.id,))
        owners = cursor.fetchall()
        if len(owners) == 0:
            embed = discord.Embed(
                title="🚫 **No hay Owners**",
                description=f'No hay owners en este servidor',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        embed = discord.Embed(
            title="👑 **Owners**",
            description="Estos son los owners de este servidor",
            color=discord.Color.green()
        )
        for owner in owners:
            embed.add_field(name="Owner", value=owner[0], inline=False)
            embed.add_field(name="ID", value=owner[1], inline=False)
        await interaction.response.send_message(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="⚠️ **Error**",
            description=f'No se ha podido listar a los owners por {e}',
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
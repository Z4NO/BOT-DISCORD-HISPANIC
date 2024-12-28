#Con este comandos podremso enviar un mensaje directo a un usuario del servidor

import discord
import sqlite3
from datetime import datetime
from comandos.SETUP_LOGS.logcontrol import logcontrol

async def send_dm(interaction: discord.Interaction, member: discord.Member, mensaje: str, cursor: sqlite3.Cursor, conn: sqlite3.Connection):
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
        
        # Comprobamos que el usuario ha completado todos los campos necesarios
        if member is None or mensaje is None:
            embed = discord.Embed(
                title="⚠️ **Error**",
                description=f'Por favor, completa todos los campos',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        #Definimos un botón el cúal nos va a llevar al servidor
        Boton = discord.ui.Button(
            style=discord.ButtonStyle.link, 
            label="Ir al servidor", 
            url=f"https://discord.com/channels/750433534581276692/850513747075530754",
            emoji="🔗"
        )
        view2 = discord.ui.View()
        view2.add_item(Boton)
        # Enviamos el mensaje al usuario
        await member.send(content=f'{member.mention}', embed=discord.Embed(
            title="📩 **Mensaje**",
            type="rich",
            description=f'{mensaje}',
            color=discord.Color.blue()),
            tts=False,
            mention_author=True,
            view=view2
            )
        embed = discord.Embed(
            title="✅ **Mensaje enviado**",
            description=f'Se ha enviado el mensaje a {member.mention}',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)

        try:
            await logcontrol(interaction, member, mensaje, cursor, "DM")
        except Exception as e:
            print(f"Error en logcontrol: {e}")
    except Exception as e:
        embed = discord.Embed(
            title="⚠️ **Error**",
            description=f'No se ha podido enviar el mensaje a {member.mention} por {e}',
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        return
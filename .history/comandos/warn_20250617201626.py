#En esta base de datos cada warn representa una fila de nuestra base de datos ,  por lo que si un usuario tiene 3 warns , tendrá 3 filas en la base de datos , por lo que si queremos saber cuantos warns tiene un usuario , debemos de contar cuantas filas tiene en la base de datos para ese usuario con el campo idUsuario

import discord
import sqlite3
from datetime import datetime
from comandos.SETUP_LOGS.logcontrol import logcontrol

def comprobar_warns(cursor: sqlite3.Cursor, member: discord.Member):
    cursor.execute("SELECT * FROM warns WHERE idUsuario = ?", (member.id,))
    warns = cursor.fetchall()
    return warns 

async def WarnMiembro(interaction: discord.Interaction, cursor: sqlite3.Cursor, member: discord.Member, reason: str, conn: sqlite3.Connection):
    try:
        # Comprobamos si el usuario es owner y si está en la base de datos
        cursor.execute("SELECT * FROM owners WHERE idDiscord = ? AND SERVER_idSERVER = ?", (interaction.user.id, interaction.guild.id))
        row = cursor.fetchone()
        if row is None or interaction.user.id != row[2]:
            embed = discord.Embed(
                title="🚫 **Permiso denegado**",
                description=f'No tienes permisos para usar este comando {interaction.user.mention}',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Comprobamos que el usuario ha completado todos los campos necesarios
        if member is None or reason is None:
            embed = discord.Embed(
                title="⚠️ **Error**",
                description=f'Por favor, completa todos los campos',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        # Añadimos el warn al usuario
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO warns (idUsuario, idModerador, reason, fecha, SERVER_idSERVER) VALUES (?, ?, ?, ?, ?)", (member.id, interaction.user.id, reason, current_date, interaction.guild.id))
        conn.commit()
        embed = discord.Embed(
            title="⚠️ **Usuario Warned**",
            description=f'{member.mention} ha sido warned por **{reason}**',
            color=discord.Color.green()
        )
        embed.set_image(url=member.avatar.url)
        await interaction.response.send_message(embed=embed)

        try:
            await logcontrol(interaction, member, reason, cursor, "Warn")
        except Exception as e:
            print(f"Error en logcontrol: {e}")

        # Añadimos el warn a la tabla de acciones de moderador
        cursor.execute("INSERT INTO moderatoractions (idModerador, actionType, afectedMember, idAfected, date, endDateAction, reason, Owners_idOwners, idSERVER) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (interaction.user.id, "warn", member.name, member.id, current_date, None, reason, row[0], interaction.guild.id))

        warns = comprobar_warns(cursor, member)
        if len(warns) >= 3:
            await member.ban(reason="Ha alcanzado el limite de warns")
            embed = discord.Embed(
                title="🔨 **Usuario baneado**",
                description=f'{member.mention} ha sido baneado por alcanzar el limite de warns',
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
            return

    except Exception as e:
        embed = discord.Embed(
            title="⚠️ **Error**",
            description=f'No se ha podido warnear al usuario {member.mention} por {e}',
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

async def DesWarnMiembro(interaction: discord.Interaction, cursor: sqlite3.Cursor, member: discord.Member, reason: str, conn: sqlite3.Connection):
    try:
        # Comprobamos si el usuario es owner y si está en la base de datos
        cursor.execute("SELECT * FROM owners WHERE idDiscord = ? AND SERVER_idSERVER = ?", (interaction.user.id, interaction.guild.id))
        row = cursor.fetchone()
        if row is None or interaction.user.id != row[2]:
            embed = discord.Embed(
                title="🚫 **Permiso denegado**",
                description=f'No tienes permisos para usar este comando {interaction.user.mention}',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Comprobamos que el usuario ha completado todos los campos necesarios
        if member is None or reason is None:
            embed = discord.Embed(
                title="⚠️ **Error**",
                description=f'Por favor, completa todos los campos',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        # Eliminamos el warn del usuario
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("DELETE FROM warns WHERE idUsuario = ? AND SERVER_idSERVER = ?", (member.id, interaction.guild.id))
        conn.commit()
        embed = discord.Embed(
            title="✅ **Usuario Deswarned**",
            description=f'{member.mention} ha sido deswarned por **{reason}**',
            color=discord.Color.green()
        )
        embed.set_image(url=member.avatar.url)
        await interaction.response.send_message(embed=embed)

        try:
            await logcontrol(interaction, member, reason, cursor, "Deswarn")
        except Exception as e:
            print(f"Error en logcontrol: {e}")

    except Exception as e:
        embed = discord.Embed(
            title="⚠️ **Error**",
            description=f'No se ha podido deswarnear al usuario {member.mention} por {e}',
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

async def CheckWarnsMiembro(interaction: discord.Interaction, cursor: sqlite3.Cursor, member: discord.Member):
    try:
        # Comprobamos si el usuario es owner y si está en la base de datos
        cursor.execute("SELECT * FROM owners WHERE idDiscord = ? AND SERVER_idSERVER = ?", (interaction.user.id, interaction.guild.id))
        row = cursor.fetchone()
        if row is None or interaction.user.id != row[2]:
            embed = discord.Embed(
                title="🚫 **Permiso denegado**",
                description=f'No tienes permisos para usar este comando {interaction.user.mention}',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return
        
        # Comprobamos los warns del usuario
        warns = comprobar_warns(cursor, member)
        if not warns:
            embed = discord.Embed(
                title="✅ **Usuario sin Warns**",
                description=f'{member.mention} no tiene warns',
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(
            title=f"⚠️ **Warns de {member.name}**",
            description=f'{member.mention} tiene {len(warns)} warns:',
            color=discord.Color.orange()
        )
        for warn in warns:
            embed.add_field(name=f"Warn #{warn[0]}", value=f"**Razón:** {warn[2]}\n**Fecha:** {warn[3]}", inline=False)
        
        await interaction.response.send_message(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title="⚠️ **Error**",
            description=f'No se han podido comprobar los warns del usuario {member.mention} por {e}',
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
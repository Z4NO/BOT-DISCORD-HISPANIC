import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta

from comandos.SETUP_LOGS.logcontrol import logcontrol

async def MutearMiembro(interaction: discord.Interaction, cursor: sqlite3.Cursor, reason: str, member: discord.Member, tiempo: str, conn: sqlite3.Connection):
    try:
        # Comprobamos si el usuario es owner y si está en la base de datos y si está en el servidor correcto
        cursor.execute("SELECT * FROM owners WHERE idDiscord = ? AND SERVER_idSERVER = ?", (interaction.user.id, interaction.guild.id))
        row = cursor.fetchone()
        if row is None or interaction.user.id != row[2]:
            embed = discord.Embed(title="🚫 **Permiso denegado**", description=f'No tienes permisos para usar este comando {interaction.user.mention}', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return
        
        if member is None or reason is None or tiempo is None:
            embed = discord.Embed(title="⚠️ **Error**", description=f'Por favor, completa todos los campos', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return

        # Procesar el tiempo (formato: "1d" para 1 día, "1h" para 1 hora, "1m" para 1 minuto)
        tiempo_delta = None
        try:
            unit = tiempo[-1].lower()
            value = int(tiempo[:-1])
            
            if unit == 'd':
                tiempo_delta = timedelta(days=value)
            elif unit == 'h':
                tiempo_delta = timedelta(hours=value)
            elif unit == 'm':
                tiempo_delta = timedelta(minutes=value)
            else:
                raise ValueError("Unidad de tiempo no válida")
                
        except ValueError:
            embed = discord.Embed(title="⚠️ **Error**", description='Formato de tiempo incorrecto. Usa: número seguido de d (días), h (horas) o m (minutos). Ejemplo: 1d, 2h, 30m', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return

        # Silenciar al usuario
        if not member.is_timed_out():
            await member.timeout(tiempo_delta, reason=reason)
            embed = discord.Embed(title="🔇 **Usuario silenciado**", description=f'{member.mention} ha sido silenciado por **{tiempo}** debido a: **{reason}**', color=discord.Color.green())
            embed.set_image(url=member.avatar.url)
            await interaction.response.send_message(embed=embed)
        
        try:
            await logcontrol(interaction, member, reason, cursor, "Mute")
        except Exception as e:
            print(f"Error en logcontrol: {e}")

        # Registrar en la base de datos
        cursor.execute("INSERT INTO moderatoractions (idModerador, actionType, afectedMember, idAfected, date, endDateAction, reason, Owners_idOwners, idSERVER) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (interaction.user.id, 'mute', member.name, member.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), None, reason, row[0], interaction.guild.id))
        conn.commit()

    except Exception as e:
        await interaction.response.send_message(f'No se ha podido silenciar a {member.name} por {e}')


async def DesmutearMiembro(interaction: discord.Interaction, cursor: sqlite3.Cursor, member: discord.Member, reason: str, conn: sqlite3.Connection):
    try:
        # Comprobamos si el usuario es owner y si está en la base de datos y si está en el servidor correcto
        cursor.execute("SELECT * FROM owners WHERE idDiscord = ? AND SERVER_idSERVER = ?", (interaction.user.id, interaction.guild.id))
        row = cursor.fetchone()
        if row is None or interaction.user.id != row[2]:
            embed = discord.Embed(title="🚫 **Permiso denegado**", description=f'No tienes permisos para usar este comando {interaction.user.mention}', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return
        
        if member is None or reason is None:
            embed = discord.Embed(title="⚠️ **Error**", description=f'Por favor, completa todos los campos', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return

        # Desilenciar al usuario
        if member.is_timed_out():
            await member.edit(timed_out_until=None)
            embed = discord.Embed(title="🔊 **Usuario desilenciado**", description=f'{member.mention} ha sido desilenciado por **{reason}**', color=discord.Color.green())
            embed.set_image(url=member.avatar.url)
            await interaction.response.send_message(embed=embed)
        
        try:
            await logcontrol(interaction, member, reason, cursor, "Des Mute")
        except Exception as e:
            print(f"Error en logcontrol: {e}")

        # Registrar en la base de datos
        cursor.execute("INSERT INTO moderatoractions (idModerador, actionType, afectedMember, idAfected, date, endDateAction, reason, Owners_idOwners, idSERVER) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (interaction.user.id, 'unmute', member.name, member.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), None, reason, row[0], interaction.guild.id))
        conn.commit()

    except Exception as e:
        await interaction.response.send_message(f'No se ha podido desilenciar a {member.name} por {e}')
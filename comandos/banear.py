import discord
from discord.ext import commands
import sqlite3
from datetime import datetime

#MODICAMOS EL COMANDO PORQUE SOLO LOS OWNER QUE ESTAN EN LA BASE DE DATOS PUEDEN USAR ESTE COMANDO Y SI ESTAN EN SU SERVIDOR (es decir un owner de un servidor no puede banear a un miembro de otro servidor en el que no esté registrado como owner aunque el bot esté en ambos servidores)  
async def banear_command(interaction: discord.Interaction, member: discord.Member, reason: str, cursor: sqlite3.Cursor, conn: sqlite3.Connection, fechafinal: str): 
    try:
        # Comprobamos si el usuario es owner y si está en la base de datos y si está en el servidor correcto
        cursor.execute("SELECT * FROM owners WHERE idDiscord = ? AND SERVER_idSERVER = ?", (interaction.user.id, interaction.guild.id))
        row = cursor.fetchone()
        if row is None or interaction.user.id != interaction.guild.owner_id:
            embed = discord.Embed(title="Permiso denegado", description=f'No tienes permisos para usar este comando {interaction.user.mention}', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return
        
        #comprobamos que el usuario ha completado todos los campos necesarios
        if member is None or reason is None or fechafinal is None:
            embed = discord.Embed(title="Error", description=f'Por favor, completa todos los campos', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return

        # Convertimos fechafinal a un objeto datetime
        try:
            fechafinal_dt = datetime.strptime(fechafinal, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            embed = discord.Embed(title="Error", description=f'El formato de la fecha final es incorrecto. Usa el formato YYYY-MM-DD HH:MM:SS', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return

        # Baneamos al usuario
        await member.ban(reason=reason)
        embed = discord.Embed(title="Usuario baneado", description=f'{member.mention} ha sido baneado por {reason}', color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

        # Añadimos el baneo a la base de datos
        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO moderatoractions (idModerador, actionType, afectedMember, idAfected, date, endDateAction, reason, Owners_idOwners, idSERVER) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (interaction.user.id, "ban", member.name, member.id, current_date, fechafinal_dt.strftime("%Y-%m-%d %H:%M:%S"), reason, interaction.user.id, interaction.guild.id))
        conn.commit()

        #MANDAMOS un embed al usuario baneado para informarle de su baneo
        embed_enviar = discord.Embed(title="Baneado", description=f'Has sido baneado del servidor {interaction.guild.name} por {reason}', color=discord.Color.red(),url=interaction.guild.icon.url)
        await member.send(content=f'{member.mention}', embed=embed_enviar)


    except Exception as e:
        embed = discord.Embed(title="Error", description=f'No se ha podido banear al usuario {member.mention} por {e}', color=discord.Color.red())
        await interaction.response.send_message(embed=embed)


async def desBanear_command(interaction: discord.Interaction, user: discord.User, reason: str, cursor: sqlite3.Cursor, conn: sqlite3.Connection): 
    try:
        # Check if command user is owner
        cursor.execute("SELECT * FROM owners WHERE idDiscord = ? AND SERVER_idSERVER = ?", (interaction.user.id, interaction.guild.id))
        row = cursor.fetchone()
        if row is None or interaction.user.id != interaction.guild.owner_id:
            embed = discord.Embed(title="Permiso denegado", description=f'No tienes permisos para usar este comando {interaction.user.mention}', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return
        
        # Check required fields
        if user is None or reason is None:
            embed = discord.Embed(title="Error", description=f'Por favor, completa todos los campos', color=discord.Color.red())
            await interaction.response.send_message(embed=embed)
            return

        # Unban user
        try:
            await interaction.guild.unban(user, reason=reason)
            embed = discord.Embed(title="Usuario Desbaneado", description=f'{user.mention} ha sido desbaneado por {reason}', color=discord.Color.green())
            await interaction.response.send_message(embed=embed)

            # Log unban action to database
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("INSERT INTO moderatoractions (idModerador, actionType, afectedMember, idAfected, date, endDateAction, reason, Owners_idOwners, idSERVER) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                         (interaction.user.id, "Desbaneo", user.name, user.id, current_date, None, reason, interaction.user.id, interaction.guild.id))
            conn.commit()

            try:
                # Notify user about unban
                embed_notify = discord.Embed(title="Desbaneado", 
                                          description=f'Has sido desbaneado del servidor {interaction.guild.name}', 
                                          color=discord.Color.green())
                await user.send(embed=embed_notify)
            except:
                pass  # Ignore if can't DM user

        except discord.NotFound:
            await interaction.response.send_message("Este usuario no está baneado.", ephemeral=True)

    except Exception as e:
        embed = discord.Embed(title="Error", description=f'No se ha podido desbanear al usuario: {str(e)}', color=discord.Color.red())
        await interaction.response.send_message(embed=embed)
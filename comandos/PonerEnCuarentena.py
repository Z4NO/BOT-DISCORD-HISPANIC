#En este comando le asigannaremos un rol a un usuario llamado cuarantena , ademas de esto le quitaremos todos losroles y solo dejaremos este rol, si no existe el rol lo crearemos notros , este rol no tendrá ningun permiso

import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta
from comandos.SETUP_LOGS.logcontrol import logcontrol


async def PonerEnCuarentena(interaction: discord.Interaction, cursor: sqlite3.Cursor, member: discord.Member, reason: str, conn: sqlite3.Connection):
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
        if member is None or reason is None:
            embed = discord.Embed(
                title="❌ **Error**",
                description=f'Por favor, completa todos los campos',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        await interaction.response.send_message("Procesando...", ephemeral=True)
        # Comprobamos si el rol de cuarentena ya existe
        roles = await interaction.guild.fetch_roles()
        rol = None
        for r in roles:
            if r.name == "Cuarentena":
                rol = r
                break
        if rol is None:
            rol = await interaction.guild.create_role(name="Cuarentena", reason="Rol para cuarentena de usuarios", permissions=discord.Permissions.none())
            for channel in interaction.guild.channels:
                await channel.set_permissions(rol, read_messages=False, send_messages=False, connect=False, speak=False, view_channel=False)
        
        # Añadimos el rol de cuarentena al usuario
        await member.add_roles(rol, reason=reason)
        embed = discord.Embed(
            title="🚨 **Usuario en cuarentena**",
            description=f'{member.mention} ha sido puesto en cuarentena por **{reason}**',
            color=discord.Color.green()
        )
        embed.set_image(url=member.avatar.url)
        await interaction.edit_original_response(content=None, embed=embed)

        try:
            await logcontrol(interaction, member, reason, cursor, "Cuarentena")
        except Exception as e:
            print(f"Error en logcontrol: {e}")

        # Añadimos el warn a la tabla de acciones de moderador
        cursor.execute("INSERT INTO moderatoractions (idModerador, actionType, afectedMember, idAfected, date, endDateAction, reason, Owners_idOwners, idSERVER) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (interaction.user.id, "cuarentena", member.name, member.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), None, reason, row[0], interaction.guild.id))
        conn.commit()

    except Exception as e:
        embed = discord.Embed(
            title="❌ **Error**",
            description=f'No se ha podido poner en cuarentena al usuario {member.mention} por {e}',
            color=discord.Color.red()
        )
        await interaction.edit_original_response(content=None, embed=embed)

async def SacarDeCuarentena(interaction: discord.Interaction, cursor: sqlite3.Cursor, member: discord.Member, reason: str, conn: sqlite3.Connection):
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
        if member is None or reason is None:
            embed = discord.Embed(
                title="❌ **Error**",
                description=f'Por favor, completa todos los campos',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        await interaction.response.send_message("Procesando...", ephemeral=True)
        # Comprobamos si el rol de cuarentena ya existe
        roles = await interaction.guild.fetch_roles()
        rol = None
        for r in roles:
            if r.name == "Cuarentena":
                rol = r
                break
        if rol is None:
            embed = discord.Embed(
                title="❌ **Error**",
                description=f'El rol de cuarentena no existe',
                color=discord.Color.red()
            )
            await interaction.edit_original_response(content=None, embed=embed)
            return
        
        # Quitamos el rol de cuarentena al usuario
        await member.remove_roles(rol, reason=reason)
        embed = discord.Embed(
            title="✅ **Usuario quitado de cuarentena**",
            description=f'{member.mention} ha sido quitado de cuarentena por **{reason}**',
            color=discord.Color.green()
        )
        embed.set_image(url=member.avatar.url)
        await interaction.edit_original_response(content=None, embed=embed)

        try:
            await logcontrol(interaction, member, reason, cursor, "Des Cuarentena")
        except Exception as e:
            print(f"Error en logcontrol: {e}")

        # Añadimos el warn a la tabla de acciones de moderador
        cursor.execute("INSERT INTO moderatoractions (idModerador, actionType, afectedMember, idAfected, date, endDateAction, reason, Owners_idOwners, idSERVER) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (interaction.user.id, "Des cuarentena", member.name, member.id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), None, reason, row[0], interaction.guild.id))
        conn.commit()

    except Exception as e:
        embed = discord.Embed(
            title="❌ **Error**",
            description=f'No se ha podido quitar de cuarentena al usuario {member.mention} por {e}',
            color=discord.Color.red()
        )
        await interaction.edit_original_response(content=None, embed=embed)
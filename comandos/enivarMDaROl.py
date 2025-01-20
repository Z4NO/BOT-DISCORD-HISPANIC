import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.ext.commands import MissingPermissions
import sqlite3
from datetime import datetime
from .SETUP_LOGS.logcontrol import logcontrol

async def enviarMDaRol(interaction: discord.Interaction, rol: discord.Role, mensaje: str, cursor: sqlite3.Cursor, url: str):
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
        if rol is None or mensaje is None or url is None:
            embed = discord.Embed(
                title="⚠️ **Error**",
                description=f'Por favor, completa todos los campos',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        # Verificamos si el bot tiene permisos para ver los miembros del rol
        if not interaction.guild.me.guild_permissions.manage_roles or not interaction.guild.me.guild_permissions.view_audit_log:
            embed = discord.Embed(
                title="⚠️ **Error de permisos**",
                description=f'El bot no tiene permisos para ver los miembros del rol {rol.mention}',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
            return

        miebros = interaction.guild.get_role(rol.id).members

        embed = discord.Embed(
            title="✅ **Interacción correcta**",
            description=f'Enviando mensaje a {len(miebros)} miembros con el rol {rol.mention}',
            color=discord.Color.green()
        )
      
        await interaction.response.send_message(embed=embed)
        Boton = discord.ui.Button(
            style=discord.ButtonStyle.link, 
            label="Ir al servidor", 
            url=f"{url}",
            emoji="🔗"
        )

        view2 = discord.ui.View()
        view2.add_item(Boton)

        for miembro in miebros:
            try:
                await miembro.send(content=f'{miembro.mention}', embed=discord.Embed(
                    title="📩 **Mensaje**",
                    type="rich",
                    description=f'{mensaje}',
                    color=discord.Color.blue()),
                    tts=False,
                    mention_author=True,
                    view=view2
                )
                print(f"Mensaje enviado a {miembro.name}")  # Mensaje de depuración
            except discord.Forbidden:
                print(f"No se pudo enviar el mensaje a {miembro.name}, falta de permisos")
            except Exception as e:
                print(f"Error al enviar el mensaje a {miembro.name}: {e}")

        embed = discord.Embed(
            title="✅ **Mensaje enviado**",
            description=f'Se ha enviado el mensaje a todos los miembros con el rol {rol.mention}',
            color=discord.Color.green()
        )
        await interaction.edit_original_response(embed=embed)

        try:
            await logcontrol(interaction, rol, mensaje, cursor, "DM A ROL")
        except Exception as e:
            print(f"Error en logcontrol: {e}")

    except Exception as e:
        print(f"Error al enviar el mensaje a los miembros con el rol: {e}")
        return False
    return True
import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta

def ObtenerCanalesGuils(guild: discord.Guild):
    lista_canales = []
    for channel in guild.text_channels:
        lista_canales.append(channel)
    return lista_canales[:25]  # Limitar a 25 canales

def ObtenerRolesGuild(guild: discord.Guild):
    lista_roles = []
    for role in guild.roles:
        lista_roles.append(role)
    return lista_roles[:25]  # Limitar a 25 roles

diccionario = {
        "idlogChannel": 0,
        "prefix": "a/",
        "idQuarentineRole": 0,
        "idmoderationChannel": 0,   
        "autoModeration": False
}

class SetupLogsChannels(discord.ui.Select):
    def __init__(self, guild: discord.Guild):
        self.guild = guild
        options = [
            discord.SelectOption(
                label=channel.name,
                value=str(channel.id)
            )
            for channel in ObtenerCanalesGuils(guild)
        ]
        super().__init__(
            placeholder='Selecciona un canal de texto para el canal de logs',
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        diccionario["idlogChannel"] = int(self.values[0])
        await interaction.response.send_message(f"Elegiste el canal {self.values[0]} para los logs", ephemeral=True)

class SetupQuarentineRole(discord.ui.Select):
    def __init__(self, guild: discord.Guild):
        self.guild = guild
        options = [
            discord.SelectOption(
                label=role.name,
                value=str(role.id)
            )
            for role in ObtenerRolesGuild(guild)
        ]
        super().__init__(
            placeholder='Selecciona un rol para la cuarentena',
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        diccionario["idQuarentineRole"] = int(self.values[0])
        await interaction.response.send_message(f"Elegiste el rol {self.values[0]} para la cuarentena", ephemeral=True)

class ConfirmButton(discord.ui.Button):
    def __init__(self, guild: discord.Guild, conn: sqlite3.Connection, cursor: sqlite3.Cursor):
        super().__init__(label="Confirmar", style=discord.ButtonStyle.green)
        self.guild = guild
        self.conn = conn
        self.cursor = cursor

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)  # Defer the response to give more time
        try:
            if diccionario["idlogChannel"] == 0 or diccionario["idQuarentineRole"] == 0:
                await interaction.edit_original_response(content="**Por favor, completa todos los campos**")
                return
            
            self.cursor.execute("SELECT * FROM server_configuration WHERE idSERVER = ?", (self.guild.id,))
            row = self.cursor.fetchone()
            message = ""
            if row is not None:
                self.cursor.execute("DELETE FROM server_configuration WHERE idSERVER = ?", (self.guild.id,))
                self.conn.commit()
                message = "**Configuración anterior eliminada.**"
            
            self.cursor.execute("INSERT INTO server_configuration (idSERVER, idlogChannel, prefix, idQuarentineRole, idmoderationChannel, autoModeration) VALUES (?, ?, ?, ?, ?, ?)",
                                (self.guild.id, diccionario["idlogChannel"], diccionario["prefix"], diccionario["idQuarentineRole"], diccionario["idmoderationChannel"], diccionario["autoModeration"]))
            self.conn.commit()
            
            await interaction.edit_original_response(content=f"{message}\n**Configuración guardada exitosamente.**")
        except Exception as e:
            await interaction.edit_original_response(content=f"**Error al guardar la configuración: {e}**")

class SetupView(discord.ui.View):
    def __init__(self, guild: discord.Guild, conn: sqlite3.Connection, cursor: sqlite3.Cursor):
        super().__init__()
        self.add_item(SetupLogsChannels(guild))
        self.add_item(SetupQuarentineRole(guild))
        self.add_item(ConfirmButton(guild, conn, cursor))
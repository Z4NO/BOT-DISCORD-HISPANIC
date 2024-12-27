#EN ESTE COMANDO VAMOS A AÑADIR UN BREVE SETUP DE LOS CANALES DE LOGS DEL SERVIDOR , ADEMÁS AÑADIREMOS LOS CAMPOS NECESARIOS EN LA BASE DE DATOS COMO:
# - idSERVER_CONFIGURATION
# - idlogChannel
# - prefix
# - idQuarentineRole
# - idmoderationChannel
# - autoModeration

#Vamos a crear un dropdown con los canales de texto del servidor
import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta

def ObtenerCanalesGuils(guild: discord.Guild):
    lista_canales = []
    for channel in guild.text_channels:
        lista_canales.append(channel)
    return lista_canales

def ObtenerRolesGuild(guild: discord.Guild):
    lista_roles = []
    for role in guild.roles:
        lista_roles.append(role)
    return lista_roles

diccionario = {
        "idlogChannel": 0,
        "prefix": "a/",
        "idQuarentineRole": 0,
        "idmoderationChannel": 0,   
        "autoModeration": False
}

class SetupLogsChannels(discord.ui.Select):
    #lo primero es que vamos a crar un diccionario/ array donde vamos a insertar los valores que elgiga el usuario para luego insertarlos en la base de datos
    #luego vamos a crear un dropdown con los canales de texto del servidor
    
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
        await interaction.response.send_message(f"Elegiste el canal {self.values[0]} para los logs")
        #añadir el canal de logs al diccionario
        diccionario["idlogChannel"] = int(self.values[0])

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
        await interaction.response.send_message(f"Elegiste el rol {self.values[0]} para la cuarentena")
        #añadir el rol de cuarentena al diccionario
        diccionario["idQuarentineRole"] = int(self.values[0])

class ConfirmButton(discord.ui.Button):
    def __init__(self, guild: discord.Guild, conn: sqlite3.Connection, cursor: sqlite3.Cursor):
        super().__init__(label="Confirmar", style=discord.ButtonStyle.green)
        self.guild = guild
        self.conn = conn
        self.cursor = cursor

    async def callback(self, interaction: discord.Interaction):
        try:
            if diccionario["idlogChannel"] == 0 or diccionario["idQuarentineRole"] == 0:
                await interaction.response.send_message("**Por favor, completa todos los campos**", ephemeral=True)
                return
            
            #Aqui debemos tener en cuenta que si el usuario ya ha configurado los logs del servidor , deberiamos borra la configuración anterior y añadir la nueva
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
            
            await interaction.response.send_message(f"{message}\n**Configuración guardada exitosamente.**", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"**Error al guardar la configuración: {e}**", ephemeral=True)



class SetpView(discord.ui.View):
    def __init__(self, guild: discord.Guild, conn: sqlite3.Connection, cursor: sqlite3.Cursor):
        super().__init__()
        self.add_item(SetupLogsChannels(guild))
        self.add_item(SetupQuarentineRole(guild))
        self.conn = conn
        self.cursor = cursor
        self.add_item(ConfirmButton(guild, conn, cursor))


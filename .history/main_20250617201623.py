import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from typing import Final
import json
import asyncio
from datetime import datetime
from comandos.MODERACIÓN.banear import banear_command, desBanear_command
from comandos.arcoiris import Arcoris
from comandos.MODERACIÓN.listaserver import ListarServerEnDb
from comandos.MODERACIÓN.añadirOwner import AñadirOwner, QuitarOwner
from comandos.MODERACIÓN.listaraccionesmoderador import ListarAccionesModerador
from comandos.MODERACIÓN.mutear import MutearMiembro, DesmutearMiembro
from comandos.warn import WarnMiembro, DesWarnMiembro
from comandos.MODERACIÓN.PonerEnCuarentena import PonerEnCuarentena, SacarDeCuarentena
from comandos.SETUP_LOGS.setuplogs import SetupView, SetupLogsChannels, SetupQuarentineRole
from comandos.SETUP_LOGS.verconfg import VerConfig
from comandos.help import Help
from comandos.MODERACIÓN.md import send_dm
from comandos.MODERACIÓN.añadirsticker import AñadirSticker
from comandos.MODERACIÓN.enivarMDaROl import enviarMDaRol
from comandos.quienes import quienes
from comandos.BuscarJuego import buscar_juego
from comandos.MODERACIÓN.listarOwner import listarOwner
from comandos.valorant_tracker import MirarTracker
from comandos.sorteos import Sorteo
import sqlite3

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
RAWG_API_KEY: Final[str] = os.getenv("RAWG_API_KEY")
HUGGINGFACE_TOKEN: Final[str] = os.getenv("HUGGINGFACE_TOKEN")

    
# Conectar a la base de datos SQLite existente
try:
    conn = sqlite3.connect('data2.sqlite')
    cursor = conn.cursor()
    print("Conectado a la base de datos SQLite")
except Exception as e:
    print(e)

server = 0

server_elegir = int(input("Introduce el servidor en el que quieres trabajar\n1 -> Para HISPANIC\n2 -> Para pruebas bot : "))
if server_elegir == 1:
    server = 750433534581276692
elif server_elegir == 2:
    server = 1006662013071675502

class Client(commands.Bot):
    async def on_ready(self):
        print('Logueado como: ', self.user)
        await client.change_presence(activity=discord.Streaming(name="HISPANIC CLAN ON TOP", url="https://discord.gg/py6vtGNedJ"))

        try:
            guild = discord.Object(id=server)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {synced} commands')
        except Exception as e:
            print(e)

        obtener_servidores()
        self.chek_tickets.start()  # Iniciar la tarea de verificación de tickets

    async def on_message(self, message):
        if message.author == self.user:
            return


    @tasks.loop(minutes=7)
    async def chek_tickets(self):
        categoria_de_tickets = obtner_categoria_tickets()
        if categoria_de_tickets is None:
            print("No se encontró la categoría de tickets")  # Mensaje de depuración
            return
        await comprobar_canal_ticket(categoria_de_tickets)
    
    @tasks.loop(minutes=7)
    async def check_sanciones(self):
        await obtener_sanciones_no_terminadas()

        
                

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = Client(command_prefix='a/', intents=intents)


async def obtener_sanciones_no_terminadas():
    #En esta función obtendremos todas las sanciones que no han terminado como los bans, cuarentena , etc para comprobar si han terminado o no, si han terminado desbanearemos a los usuaarios y les quitaremos el rol de cuarentena
    cursor.execute("SELECT actionType, endDateAction, idAfected FORM moderatoractions WHERE endDateAction < ?", (datetime.now(),))
    rows = cursor.fetchall()
    guild = client.fetch_guild(server)
    for row in rows:
        if row[0] == "ban":
            try:
                await guild.unban(discord.Object(id=row[2]), reason = f"Sanción terminada {row[0]}")
                print(f"Usuario {row[2]} desbaneado")
            except Exception as e:
                print(f"Error al desbanear al usuario {row[2]}: {e}")
        elif row[0] == "cuarentena":
            try:
                member = await guild.fetch_member(row[2])
                role = discord.utils.get(guild.roles, name="Cuarentena")
                await member.remove_roles(role)
                print(f"Usuario {row[2]} sacado de la cuarentena")
            except Exception as e:
                print(f"Error al sacar de la cuarentena al usuario {row[2]}: {e}")



async def crear_embed_ticket_enviar(canal: discord.TextChannel):
    embed = discord.Embed(
                    title="Nuevo ticket",
                    description="Se ha creado un nuevo ticket",
                    color=discord.Color.green(),
                    type="rich"
                )
    embed.set_footer(text="HISPANIC BOT")
    try:
        await canal.send(f"<@&764955070500438016>", embed=embed)
        print(f"Mensaje enviado en el canal {canal.name}")  # Mensaje de depuración
    except discord.Forbidden:
        print(f"Error: No tengo permisos para enviar mensajes en el canal {canal.name}")
    except Exception as e:
        print(f"Error al enviar el mensaje en el canal {canal.name}: {e}")

async def comprobar_canal_ticket(categoria: discord.CategoryChannel):
    for channel in categoria.text_channels:
            print(f"Verificando canal: {channel.name}")  # Mensaje de depuración
            if not channel.name.startswith("ticket📈-") and not channel.name.startswith("closed-"):
                new_name = "ticket📈-" + channel.name.split("ticket-")[1]
                print(f"Cambiando nombre del canal {channel.name} a {new_name}")  # Mensaje de depuración
                try:
                    await channel.edit(name=new_name)
                    print(f"Nombre del canal cambiado a {new_name}")  # Mensaje de depuración
                except discord.Forbidden:
                    print(f"Error: No tengo permisos para editar el canal {channel.name}")
                except Exception as e:
                    print(f"Error al cambiar el nombre del canal {channel.name}: {e}")
                await crear_embed_ticket_enviar(channel)

def obtener_servidores():
    try:
        for guild in client.guilds:
            cursor.execute("SELECT * FROM SERVER WHERE idSERVER = ?", (guild.id,))
            row = cursor.fetchone()
            if row is None:
                cursor.execute("INSERT INTO SERVER (idSERVER, serverName) VALUES (?, ?)", (guild.id, guild.name))
                conn.commit()
                print(f"Se ha añadido el servidor {guild.name} a la base de datos")
            else:
                print(f"El servidor {guild.name} ya existe en la base de datos")
    except Exception as e:
        print("Error al obtener los servidores: ", e)

def obtener_categorias(guild: discord.Guild):
    for categoria in guild.categories:
        if categoria.id == 1314262440510226553:
            return categoria

def obtner_categoria_tickets():
    try:
        categoria_tickets = None
        for guild in client.guilds:
            if guild.id == 750433534581276692:
                categoria_tickets = obtener_categorias(guild)
                break
        return categoria_tickets
    except Exception as e:
        print(f"Error al obtener la categoria de tickets: {e}")
        return None
    





GUILD_ID = discord.Object(id=server)

@client.tree.command(name='decir', description='Dice algo que tu le digas', guild=GUILD_ID)
async def DecirHola(interaction: discord.Interaction, contenido: str):
    await interaction.response.send_message(f'{contenido}')

@client.tree.command(name='decirr', description='Dice algo que tu le digas', guild=GUILD_ID)
async def DecirHola(interaction: discord.Interaction, contenido: str):
    await interaction.response.send_message(f'{contenido}')

@client.tree.command(name='banear', description='Banea a un usuario', guild=GUILD_ID)
async def banear(interaction: discord.Interaction, member: discord.Member, reason: str, fechafinal: str):
    await banear_command(interaction, member, reason, cursor, conn, fechafinal)

@client.tree.command(name='arcoiris', description='Cambia el color de un rol durante 2 minutos', guild=GUILD_ID)
async def arcoiris(interaction: discord.Interaction, rol: discord.Role):
    await Arcoris(interaction, rol)

@client.tree.command(name='listar', description='Lista los servidores en los que está el bot', guild=GUILD_ID)
async def listar(interaction: discord.Interaction):
    await ListarServerEnDb(interaction, cursor)

@client.tree.command(name='añadirowner', description='Añade un owner a un servidor', guild=GUILD_ID)
async def añadirOwner(interaction: discord.Interaction, member: discord.Member):
    await AñadirOwner(interaction, member, cursor, conn)

@client.tree.command(name='listaracciones', description='Lista las acciones realizadas por un moderador', guild=GUILD_ID)
async def listaracciones(interaction: discord.Interaction, miembro: discord.Member):
    await ListarAccionesModerador(interaction, cursor, miembro)

@client.tree.command(name='desbanear', description='Desbanea a un usuario', guild=GUILD_ID)
async def desbanear(interaction: discord.Interaction, id_user: str, reason: str):
    try:
        user = await client.fetch_user(int(id_user))
        await desBanear_command(interaction, user, reason, cursor, conn)
    except ValueError:
        await interaction.response.send_message("ID de usuario inválido", ephemeral=True)

@client.tree.command(name='mutear', description='Mutea a un usuario', guild=GUILD_ID)
async def mutear(interaction: discord.Interaction, member: discord.Member, reason: str, tiempo: str):
    await MutearMiembro(interaction, cursor, reason, member, tiempo, conn)

@client.tree.command(name='desmutear', description='Desmutea a un usuario', guild=GUILD_ID)
async def desmutear(interaction: discord.Interaction, member: discord.Member, reason: str):
    await DesmutearMiembro(interaction, cursor, member, reason, conn)

@client.tree.command(name='warn', description='Avisa a un usuario', guild=GUILD_ID)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    await WarnMiembro(interaction, cursor, member, reason, conn)

@client.tree.command(name='deswarn', description='Desavisa a un usuario', guild=GUILD_ID)
async def deswarn(interaction: discord.Interaction, member: discord.Member, reason: str):
    await DesWarnMiembro(interaction, cursor, member, reason, conn)

@client.tree.command(name='setuplogs', description='Configura los logs del servidor', guild=GUILD_ID)
async def setuplogs(interaction: discord.Interaction):
    view = SetupView(interaction.guild, conn, cursor)
    await interaction.response.send_message("Procesando...", ephemeral=True)
    try:
        await interaction.edit_original_response(content="Selecciona un canal de texto para los logs", view=view)
    except Exception as e:
        print(f"Error en setuplogs: {e}")

@client.tree.command(name='ponercuarentena', description='Pone a un usuario en cuarentena', guild=GUILD_ID)
async def ponercuarentena(interaction: discord.Interaction, member: discord.Member, reason: str):
    await PonerEnCuarentena(interaction, cursor, member, reason, conn)

@client.tree.command(name='verconfig', description='Muestra la configuración del servidor', guild=GUILD_ID)
async def verconfig(interaction: discord.Interaction):
    await VerConfig(interaction, cursor)

@client.tree.command(name='sacarcuarentena', description='Saca a un usuario de cuarentena', guild=GUILD_ID)
async def sacarcuarentena(interaction: discord.Interaction, member: discord.Member, reason: str):
    await SacarDeCuarentena(interaction, cursor, member, reason, conn)

@client.tree.command(name='help', description='Muestra los comandos disponibles', guild=GUILD_ID)
async def help(interaction: discord.Interaction):
    await Help(interaction)

@client.tree.command(name='enviar_md', description='Envía un mensaje privado a un usuario', guild=GUILD_ID)
async def senddm(interaction: discord.Interaction, member: discord.Member, mensaje: str):
    await send_dm(interaction, member, mensaje, cursor, conn)

@client.tree.command(name='añadirsticker', description='Añade un sticker al servidor', guild=GUILD_ID)
async def añadirsticker(interaction: discord.Interaction, nombre_sticker: str, descripcion_sticker: str, archivo: discord.Attachment):
    await AñadirSticker(interaction, nombre_sticker, descripcion_sticker, archivo)

@client.tree.command(name='enviar_md_rol', description='Envía un mensaje a todos los miembros con un rol', guild=GUILD_ID)
async def enviar_md_rol(interaction: discord.Interaction, rol: discord.Role, mensaje: str, url_canal: str):
    await enviarMDaRol(interaction, rol, mensaje,  cursor,  url_canal)

@client.tree.command(name='quienes', description='Muestra información de un usuario', guild=GUILD_ID)
async def mostrar_quienes(interaction: discord.Interaction, member: discord.Member):
    await quienes(interaction, member)

@client.tree.command(name='buscar_juego', description='Busca un juego en la base de datos de RAWG', guild=GUILD_ID)
async def buscar_juego_command(interaction: discord.Interaction, juego: str):
    await buscar_juego(interaction, juego, RAWG_API_KEY)

@client.tree.command(name='listarowners', description='Lista a los owners del servidor', guild=GUILD_ID)
async def listarowners(interaction: discord.Interaction):
    await listarOwner(interaction, cursor)

@client.tree.command(name='quitar_owner', description='Quita a un owner del servidor', guild=GUILD_ID)
async def quitar_owner(interaction: discord.Interaction, member: discord.Member):
    await QuitarOwner(interaction, member, cursor, conn)


@client.tree.command(name='sorteo', description='Realiza un sorteo', guild=GUILD_ID)
async def sorteo(interaction: discord.Interaction, canal: discord.TextChannel):
    await Sorteo(interaction, canal)


async def main():
    await client.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
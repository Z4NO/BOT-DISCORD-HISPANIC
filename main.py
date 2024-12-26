import discord
from discord import message
from discord.ext import commands, tasks
from discord import  app_commands
import os
from dotenv import load_dotenv
from typing import Final
import asyncio
from datetime import datetime
from comandos.banear import  banear_command, desBanear_command
from comandos.arcoiris import  Arcoris
from comandos.listaserver import ListarServerEnDb
from comandos.añadirOwner import AñadirOwner
from comandos.listaraccionesmoderador import ListarAccionesModerador
from comandos.mutear import MutearMiembro, DesmutearMiembro
from comandos.warn  import WarnMiembro, DesWarnMiembro
import sqlite3

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

"""
📚 All the different types of Events:
on_ready()
on_message(message)
on_message_edit(before, after)
on_message_delete(message)
on_member_join(member)
on_member_remove(member)
on_member_update(before, after)
on_guild_join(guild)
on_guild_remove(guild)
on_reaction_add(reaction, user)
on_reaction_remove(reaction, user)
"""

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

        try:
            guild = discord.Object(id=server)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {synced} commands')
        except Exception as e:
            print(e)

        obtener_servidores()

    async def on_message(self, message):
       
        if message.author == self.user: 
            return 
        
        if '@everyone' in message.content:
            await message.channel.send(f'{message.author.mention} ha mencionado a todos con @everyone')


        if self.user in  message.mentions:
            await message.channel.send(f'Hola {message.author.mention}! ¿En qué puedo ayudarte?')

    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send(f'{user.mention} ha reaccionado a un mensaje con {reaction.emoji}')
    
    @tasks.loop(minutes=1)
    async def check_sanciones(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("SELECT * FROM moderatoractions WHERE endDateAction <= ?", (now,))
        sanciones = cursor.fetchall()
        for sancion in sanciones:
            guild = self.get_guild(sancion[1])
            member = guild.get_member(sancion[4])
            tipo = sancion[2]
            if member:
                #Aqui debemos de distinguir que tipo de sanción es para poder saber que tipo de acción realizar , si es un ban o un mute , etc
                #tanbien debemos tener en cuenta que un usuario pueda haber  desbaneado o desmuteado al usuario de forma manual . por lo que debemos de comprobar si el usuario sigue baneado o muteado
                if tipo == "ban" and member not in await guild.bans():
                    await guild.unban(member)
                elif tipo == "mute" and guild.get_member(sancion[4]).is_timed_out():
                    await member.remove_roles(guild.get_role(sancion[5]))
                
                


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix='a/', intents=intents)

#VAMOS A CREAR UN METODO EL CUAL VA A RECOPILAR TODOS LOS SERVIDORES EN LOS QUE ESTE EL BOT Y LOS INTRODUCIRA EN LA BASE DE DATOS
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





GUILD_ID = discord.Object(id=server)
#750433534581276692 HISPANIC SERVER
#1006662013071675502 SERVIDOR DE PRUEBA


@client.tree.command(name='decir', description='Dice algo que tu le digas', guild=GUILD_ID)
#Funcion para banear a un usuario
async def DecirHola(interaction: discord.Interaction, contenido: str):
    await interaction.response.send_message(f'{contenido}')


@client.tree.command(name='decirr', description='Dice algo que tu le digas', guild=GUILD_ID)
#Funcion para banear a un usuario
async def DecirHola(interaction: discord.Interaction, contenido: str):
    await interaction.response.send_message(f'{contenido}')

@client.tree.command(name='banear', description='Banea a un usuario', guild=GUILD_ID)
async def banear(interaction: discord.Interaction , member: discord.Member, reason: str, fechafinal: str):
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


    
    

async def main():
    await client.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())

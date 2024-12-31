#En este comando se enviará un mensage en forma de embed el cuál contenga todos los comandos que el bot tiene disponibles y su descripción

import discord
from discord.ext import commands
from datetime import datetime, timedelta

async def Help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Comandos disponibles",
        description="Aquí tienes una lista de los comandos disponibles y su descripción",
        color=discord.Color.blue()
    )
    commands_list = [
        ("🔇 **/mute**", "Silencia a un miembro"),
        ("🔊 **/desmute**", "Desmutea a un miembro"),
        ("🚨 **/cuarentena**", "Pone a un miembro en cuarentena"),
        ("🛡️ **/sacardecuarentena**", "Saca a un miembro de cuarentena"),
        ("⚠️ **/warn**", "Warn a un miembro"),
        ("✅ **/deswarn**", "Deswarn a un miembro"),
        ("👑 **/añadirowner**", "Añade un owner al servidor"),
        ("🔨 **/banear**", "Banea a un miembro del servidor"),
        ("🔓 **/desbanear**", "Desbanea a un miembro"),
        ("📋 **/listaracciones**", "Lista las acciones de un moderador"),
        ("⚙️ **/setuplogs**", "Configura los logs del servidor"),
        ("🔍 **/verconfig**", "Muestra la configuración del servidor"),
        ("📜 **/listar**", "Lista los servidores en los que está el bot"),
        ("📝 **/añadirsticker**", "Añade un sticker al servidor"),
    ]
    
    for name, value in commands_list:
        embed.add_field(name=name, value=value, inline=False)
    
    await interaction.response.send_message(embed=embed)

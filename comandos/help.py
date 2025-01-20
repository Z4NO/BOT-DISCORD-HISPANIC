#En este comando se enviará un mensage en forma de embed el cuál contenga todos los comandos que el bot tiene disponibles y su descripción

#Vamos a separar los comandos por categorías donde el usuario en dsicord pueda selecciona la categoría que desee y se le muestren los comandos de esa categoría con un select menu

import discord
import discord
from datetime import datetime


commands_list_mod = [
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
        ("📤 **/enviar_md_rol** ", "Envía un mensaje directo a todos los miembros con un rol específico")
    ]
    

commands_list_utilidades = [
        ("📝 **/añadirsticker**", "Añade un sticker al servidor"),
        ("📜 **/listar**", "Lista los servidores en los que está el bot"),
        ("🎮 **/buscar_juego**", "Busca cualquier juego  y muestra información sobre él"),
        ("🤖 **/ia**", "Pregunta a la IA cualquier cosa"),
        ("📸 **/imagen**", "Genera una imagen a partir de un texto"),
    ]

class SeleccionCategoria(discord.ui.View):
    def __init__(self):
        super().__init__()
        select = discord.ui.Select(
            placeholder='Selecciona una categoría',
            min_values=1,
            max_values=1,
            options=[
                discord.SelectOption(
                    label="Moderación",
                    value="Moderación",
                    emoji="🛠️"
                ),
                discord.SelectOption(
                    label="Utilidades",
                    value="Utilidades",
                    emoji="🔧"
                )
            ]
        )
        select.callback = self.select_callback
        self.add_item(select)
    
    async def select_callback(self, interaction: discord.Interaction):
        if interaction.data['values'][0] == "Moderación":
            embed = discord.Embed(
                title="Comandos de moderación",
                description="Aquí tienes una lista de los comandos de moderación disponibles y su descripción",
                color=discord.Color.blue()
            )
            for name, value in commands_list_mod:
                embed.add_field(name=name, value=value, inline=False)
            await interaction.response.edit_message(embed=embed)
        elif interaction.data['values'][0] == "Utilidades":
            embed = discord.Embed(
                title="Comandos de utilidades",
                description="Aquí tienes una lista de los comandos de utilidades disponibles y su descripción",
                color=discord.Color.blue()
            )
            for name, value in commands_list_utilidades:
                embed.add_field(name=name, value=value, inline=False)
            await interaction.response.edit_message(embed=embed)

async def Help(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Comandos disponibles",
        description="Aquí tienes una lista de los comandos disponibles y su descripción",
        color=discord.Color.blue()
    )
    

    for name, value in commands_list_utilidades:
        embed.add_field(name=name, value=value, inline=False)
    
    try:
        await interaction.response.send_message(embed=embed, ephemeral=True, view=SeleccionCategoria())
    except Exception as e:
        await print(f"Erorr: {e}")

    
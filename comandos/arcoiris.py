import discord
from discord.ext import commands
import time

async def Arcoris(interaction: discord.Interaction, rol: discord.Role):
    try:
        if interaction.user.guild_permissions.administrator:
            # Durante dos minutos el color cambiará cada 1 segundo
            try:
                await interaction.response.send_message(f'Cambiando el color del rol {rol.mention} durante 2 minutos')
                for i in range(120):
                    await rol.edit(color=discord.Colour.random())
                    time.sleep(1)
            except Exception as e:
                await interaction.followup.send(f'No se ha podido cambiar el color del rol {rol.mention} por {e}')
        else:
            await interaction.response.send_message(f'No tienes permisos de administrador {interaction.user.mention}')
    except Exception as e:
        await interaction.response.send_message(f'No se ha podido cambiar el color del rol {rol.mention} por {e}')
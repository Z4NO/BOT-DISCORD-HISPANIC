import discord
from discord.ext import commands
import time

async def Arcoris(interaction: discord.Interaction, rol: discord.Role):
    try:
        if interaction.user.guild_permissions.administrator:
            # Durante dos minutos el color cambiará cada 1 segundo
            try:
                embed = discord.Embed(
                    title="🌈 **Cambio de color**",
                    description=f'Cambiando el color del rol {rol.mention} durante 1 hora',
                    color=discord.Color.blue()
                )
                await interaction.response.send_message(embed=embed)
                for i in range(120):
                    await rol.edit(color=discord.Colour.random())
                    time.sleep(1)
            except Exception as e:
                embed = discord.Embed(
                    title="⚠️ **Error**",
                    description=f'No se ha podido cambiar el color del rol {rol.mention} por {e}',
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
        else:
            embed = discord.Embed(
                title="🚫 **Permiso denegado**",
                description=f'No tienes permisos de administrador {interaction.user.mention}',
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title="⚠️ **Error**",
            description=f'No se ha podido cambiar el color del rol {rol.mention} por {e}',
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
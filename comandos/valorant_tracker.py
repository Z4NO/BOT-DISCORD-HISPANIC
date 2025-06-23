import discord
import requests

async def MirarTracker(interaction: discord.Interaction, Nombre: str, Tag: str):
    try:
        await interaction.response.defer(ephemeral=True)  # Diferir la respuesta para evitar el error de tiempo

        url = 'https://magicloops.dev/api/loop/76b0751d-7e6b-4a26-831c-7617f791e075/run'
        params = {"player_name": Nombre, "player_tag": Tag}

        response = requests.get(url, params=params)
        responseJson = response.json()

        player_name = responseJson.get("player_name", "N/A")
        player_tag = responseJson.get("player_tag", "N/A")
        current_rating = responseJson.get("current_rating", "N/A")
        peak_rating = responseJson.get("peak_rating", "N/A")
        top_weapons = responseJson.get("top_weapons", {})

        embed = discord.Embed(
            title=f"👑 **Tracker de Valorant - {player_name}#{player_tag}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Current Rating", value=current_rating, inline=True)
        embed.add_field(name="Peak Rating", value=peak_rating, inline=True)

        weapons_info = "\n".join([f"{weapon}: {kills}" for weapon, kills in top_weapons.items()])
        embed.add_field(name="Top Weapons", value=weapons_info, inline=False)

        await interaction.followup.send(embed=embed)  # Enviar la respuesta diferida
    except Exception as e:
        embed = discord.Embed(
            title="⚠️ **Error**",
            description=f'No se ha podido buscar el tracker por {e}',
            color=discord.Color.red()
        )
        await interaction.followup.send(embed=embed)  # Enviar la respuesta diferida en caso de error
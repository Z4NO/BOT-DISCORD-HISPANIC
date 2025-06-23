import requests
import discord


async def check_if_user_is_logged_for_spotify(interaction: discord.Interaction):
    id = username.id
    url = f"http://localhost:5000/check_if_user_is_logged/{id}"
    response = requests.get(url)
    data = response.json()
    is_logged_in = data.get("is_logged_in")
    
    if is_logged_in:
        embed = discord.Embed(
            title="✅ **Usuario conectado a Spotify**",
            description=f'{username.mention} está conectado a Spotify.',
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
    else:
        embed = discord.Embed(
            title="❌ **Usuario no conectado a Spotify**",
            description=f'{username.mention} no está conectado a Spotify.',
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
import discord
import requests

async def Sorteo(interaction: discord.Interaction, Canal: discord.channel.TextChannel): 
    mensaje_embded = discord.Embed( 
        title = " <a:giveaway:908688273218625556> **NUEVO SORTEO** <a:giveaway:908688273218625556>", 
        description = "Gente HISPANIC CLAN está sorteando alguna de estas opciones a tu elección:\n\n <:spotify:908686126599000094> **Spotify Premium**\n <a:rasengan:908686551993692221> **Dos tarjetas de crunchy rol**\n <a:money:908685366184271923> **Robux**\n <a:green_yes:908667433714343967> **Una tarjeta de 10euros del lol**\n\n Para participar solo teneís que invitar a **3 amigos** al servidor  con una invite creada por ti <a:Talking:908668043658412064>",
        color = discord.Color.green()
    )
    mensaje_embded.set_image(url="https://media.discordapp.net/attachments/850513780303462410/905479288889958480/hola.gif?ex=67a57e8d&is=67a42d0d&hm=c84c51121ddda79b6bc119ecfb3b4e7916d4b2af335c14aa55bfc0fd89da84b6&=")
    mensaje_embded.set_footer(text="El sorteo finaliza el 15 de febrero")
    await Canal.send(embed=mensaje_embded)
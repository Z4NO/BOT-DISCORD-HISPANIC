#Este archivo se encarga de manadar los logs al canal establecido en la base de datos de cada servidor , cuando una acciond e moderador ocurra se enviará un mensaje al canal de logs de ese servidor. 

#estableceremos una funcion llamada logcontrol que recibirá los parametros de la accion realizada, el moderador que la realizó y el miembro al que se le realizó la accion y la interracion que se realizó para luego enviar un mensaje al canal de logs del servidor.
import discord
import sqlite3
from datetime import datetime

async def logcontrol(interaction: discord.Interaction, member: discord.Member, reason: str, cursor: sqlite3.Cursor, tipo_accion: str):
    try:
        #Obtenemos el canal de logs para el servidor que está llamando a la interacción
        cursor.execute("SELECT idlogChannel FROM server_configuration WHERE idSERVER = ?", (interaction.guild.id,))
        row = cursor.fetchone()
        if row is None:
            await interaction.response.send_message("No se ha configurado el canal de logs para este servidor", ephemeral=True)
            return
        canal = interaction.guild.get_channel(row[0])
        if canal is None:
            await interaction.response.send_message("No se ha podido caragar el canal de logs para enivar  las notificaciones", ephemeral=True)
            return
        descripcion = f"👁️ **Responsable:** {interaction.user.mention}\n🔨 **Ación**:  **{tipo_accion}**\n🎯 **Hacia:** {member.mention}\n⭐ **Con la razón:** **{reason}**"
        embed = discord.Embed(
            colour=discord.Colour.light_gray(),
            title=f"{tipo_accion} realizada hacia: {member.name}",
            timestamp=datetime.now(),
            description=descripcion
        )
        embed.set_author(name=interaction.user.name, icon_url=interaction.user.avatar.url)
        #Definimos un boton para ver el perfil del usuario afectado
        boton = discord.ui.Button(
            style=discord.ButtonStyle.link, 
            label="Ver Perfil", 
            url=f"https://discord.com/users/{member.id}",
            emoji="🔗"
        )
        #Añadimos el boton al embed
        embed.set_footer(text=f"ID: {member.id}")
        view = discord.ui.View()
        view.add_item(boton)
        await canal.send(embed=embed, view=view)
    except Exception as e:
        print(f"Error al enviar el log: {e}")
        return False
    return True
"""
Esta clase se encarga de realizar la limpieza de los mensajes que se envian en el chat los cuales sean identicados como tóxicos por Detoxify.
Tengo pensado que esta clase se ejecute en un hilo aparte para que no afecte el rendimiento del bot.
Además, esta clase solo devolverá un booleano, si es True, el mensaje es apto para ser enviado, si es False, el mensaje no es apto para ser enviado.
"""

import detoxify
from detoxify import Detoxify
import discord
import json
import torch


# Cargamos el modelo una sola vez como variable global
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = Detoxify('multilingual', device=device)
resultado = model.predict("Hola, como estas?")
print(resultado)


async def Detoxify(message: discord.Message, config) -> bool:
    try:

        # Obtenemos el modelo de Detoxify y lo definimos como multilingual para poder operar con el español
        model = detoxify.Detoxify('multilingual')

        # Obtenemos el resultado de la predicción
        resultado  = model.predict(message.content)

        

        

    except Exception as e:
        print(f"Error al predecir el mensaje: {e}")
        return False
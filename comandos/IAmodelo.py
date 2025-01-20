from huggingface_hub import InferenceClient
import discord
import json
import datetime
import os


# Inicializar el cliente de Hugging Face
def init_llm_client(token, modelo: str):
    try:
        client = InferenceClient(model=modelo,token=token, timeout=120)
        return client
    except Exception as e:
        print(f"Error al iniciar el cliente de IA: {e}")
        return None

# Realizar una llamada al modelo de generación de texto
def llamada_llm(inference: InferenceClient, prompt: str):
    try:
        # Uso correcto del método text_generation
        respuesta = inference.text_generation(
            prompt=prompt,           # El prompt que se enviará
            max_new_tokens=400       # Máximo de tokens en la respuesta
        )
        return respuesta  # Retorna la respuesta generada
    except Exception as e:
        print(f"Error al realizar la llamada a la API: {e}")
        return "Error al procesar la solicitud."

# Pregunta a la IA desde Discord
async def Pregunta_a_ia(interaction: discord.Interaction, prompt: str, token: str):
    
    try:
        await interaction.response.send_message("Estoy pensando...", ephemeral=True)
        
        # Inicializar cliente y realizar solicitud
        inference = init_llm_client(token, "microsoft/Phi-3-mini-4k-instruct")
        if inference is None:
            raise ValueError("No se pudo inicializar el cliente de IA.")
        
        respuesta = llamada_llm(inference, prompt)


        #Vamos a definir como va a ser el embed de la respuesta
        embed = discord.Embed(
            title=f"Respuesta de la IA hacia {prompt}",
            description=f'**{respuesta}**',
            color=discord.Color.green()
        )

        embed.set_thumbnail(url=interaction.user.avatar.url)

        await interaction.edit_original_response(content=None, embed=embed)
    except Exception as e:
        await interaction.followup.send(f"Error: {e}", ephemeral=True)
        print(f"Error: {e}")

async def generar_imagen(interaction: discord.Interaction, prompt: str, token: str):
    await interaction.response.send_message("Estoy pensando...", ephemeral=True)

    # Inicializamos el cliente con el modelo de generación de imágenes.
    inference = init_llm_client(token, "stabilityai/stable-diffusion-2-1")
    if inference is None:
        await interaction.followup.send("Error al inicializar cliente.", ephemeral=True)
        return

    try:
        # Cambiar llamada para utilizar imagen en vez de texto
        image = inference.text_to_image(
            prompt=prompt,           # El prompt de la imagen a generar
            size="1024x1024",        # Tamaño de la imagen
        )

        # Guardar la imagen temporalmente
        image_path = "temp_image.png"
        image.save(image_path)

        try:
            # Enviar la imagen como archivo
            with open(image_path, "rb") as file:
                imagen_discord = discord.File(file)
                await interaction.followup.send(content="¡Aquí está tu imagen!", file=imagen_discord)
        except Exception as e:
            await interaction.followup.send(f"Error al enviar la imagen: {e}", ephemeral=True)
            return
        finally:
            # Aseguramos que la imagen temporal se borre
            if os.path.exists(image_path):
                os.remove(image_path)
    
    except Exception as e:
        # Manejo de excepciones en caso de que falle la generación de la imagen
        await interaction.followup.send(f"Error al generar la imagen: {e}", ephemeral=True)
        return


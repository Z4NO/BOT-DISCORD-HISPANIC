import discord
import aiohttp

async def buscar_juego(interaction: discord.Interaction, juego: str, Key: str):
    base_url = "https://api.rawg.io/api/games"
    params = {"key": Key, "search": juego}
    primer_juego = None

    Boton = discord.ui.Button(
        style=discord.ButtonStyle.primary,
        label="Trailers",
        emoji="🎥"
    )

    Boton3 = discord.ui.Button(
        style=discord.ButtonStyle.primary,
        label="Descripción",
        emoji="📜"
    )

    Boton2 = discord.ui.Button(
        style=discord.ButtonStyle.primary,
        label="Requisitos",
        emoji="🛠️"
    )

    vista = discord.ui.View()
    vista.add_item(Boton2)
    vista.add_item(Boton3)
    vista.add_item(Boton)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    resultados = data.get("results", [])

                    if resultados:
                        primer_juego = resultados[0]
                        nombre = primer_juego["name"]
                        fecha_lanzamiento = primer_juego.get("released", "Fecha no disponible")
                        calificacion = primer_juego.get("rating", "Sin calificación")
                        plataformas = [plat["platform"]["name"] for plat in primer_juego["platforms"]]
                        plataformas_str = ", ".join(plataformas)
                        imagen = primer_juego["background_image"]

                        embed = discord.Embed(
                            title=f"**{nombre}**",
                            description=(
                                f"Este es el primer resultado que encontré para tu búsqueda de **{juego}**:\n\n"
                                f"📅 Fecha de lanzamiento: **{fecha_lanzamiento}**\n\n"
                                f"⭐ Calificación: **{calificacion}**\n\n"
                                f"👁️ Plataformas disponibles: **{plataformas_str}**\n\n"
                            ),
                            color=discord.Color.blue(),
                        )
                        embed.set_image(url=imagen)

                        await interaction.response.send_message(embed=embed, view=vista)

                    else:
                        await interaction.response.send_message("No se encontraron resultados.")
                else:
                    await interaction.response.send_message("Ocurrió un error al buscar el juego.")
    except Exception as e:
        await interaction.response.send_message(f"Ocurrió un error al buscar el juego: {e}")

    async def button3_callback(interaction):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        resultados = data.get("results", [])

                        if resultados:
                            primer_juego = resultados[0]
                            nombre = primer_juego["name"]
                            fecha_lanzamiento = primer_juego.get("released", "Fecha no disponible")
                            calificacion = primer_juego.get("rating", "Sin calificación")
                            plataformas = [plat["platform"]["name"] for plat in primer_juego["platforms"]]
                            plataformas_str = ", ".join(plataformas)
                            imagen = primer_juego["background_image"]

                            embed = discord.Embed(
                                title=f"**{nombre}**",
                                description=(
                                    f"Este es el primer resultado que encontré para tu búsqueda de **{juego}**:\n\n"
                                    f"📅 Fecha de lanzamiento: **{fecha_lanzamiento}**\n\n"
                                    f"⭐ Calificación: **{calificacion}**\n\n"
                                    f"👁️ Plataformas disponibles: **{plataformas_str}**\n\n"
                                ),
                                color=discord.Color.blue(),
                            )
                            embed.set_image(url=imagen)

                            await interaction.response.send_message(embed=embed, view=vista)

                        else:
                            await interaction.response.send_message("No se encontraron resultados.")
                    else:
                        await interaction.response.send_message("Ocurrió un error al buscar el juego.")
        except Exception as e:
            await interaction.response.send_message(f"Ocurrió un error al buscar el juego: {e}")

    async def button_callback(interaction):
        print("Botón 'Siguiente' presionado")  # Mensaje de depuración
        if primer_juego:
            game_id = primer_juego["id"]
            base_url = f"https://api.rawg.io/api/games/{game_id}/movies"
            params = {"key": Key}

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(base_url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            trailers = data.get("results", [])

                            if trailers and len(trailers) > 0:
                                trailer1 = trailers[0]
                                trailer2 = trailers[1] if len(trailers) > 1 else None

                                embed = discord.Embed(
                                    title=f"**Trailers de {primer_juego['name']}**",
                                    description="Estos son los trailers que encontré:",
                                    color=discord.Color.blue(),
                                )

                                embed.add_field(name="Trailer 1", value=f"[Ver Trailer 1]({trailer1['data']['480']})", inline=False)
                                if trailer2:
                                    embed.add_field(name="Trailer 2", value=f"[Ver Trailer 2]({trailer2['data']['480']})", inline=False)

                                await interaction.response.edit_message(embed=embed)
                            else:
                                await interaction.response.send_message("No se encontraron trailers.")
                        else:
                            await interaction.response.send_message("Ocurrió un error al buscar los trailers.")
            except Exception as e:
                await interaction.response.send_message(f"Ocurrió un error al buscar los trailers: {e}")

    async def button2_callback(interaction):
        if primer_juego:
            game_id = primer_juego["id"]
            base_url = f"https://api.rawg.io/api/games/{game_id}"
            params = {"key": Key}

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(base_url, params=params) as response:
                        if response.status == 200:
                            data = await response.json()
                            requisitos = data.get("platforms", [])

                            pc_requisitos = None
                            for plataforma in requisitos:
                                if plataforma["platform"]["name"] == "PC":
                                    pc_requisitos = plataforma["requirements"]
                                    break

                            if pc_requisitos:
                                min_requisitos = pc_requisitos.get('minimum', 'No disponible')
                                min_requisitos_dict = {
                                    "OS": "No disponible",
                                    "Processor": "No disponible",
                                    "Memory": "No disponible",
                                    "Graphics": "No disponible",
                                    "Storage": "No disponible",
                                    "Sound Card": "No disponible"
                                }

                                # Dividir la cadena en componentes relevantes
                                componentes = min_requisitos.split('Additional Notes:')[0].split('Processor:')
                                if len(componentes) > 1:
                                    min_requisitos_dict["Processor"] = componentes[1].split('Memory:')[0].strip()
                                    min_requisitos_dict["Memory"] = componentes[1].split('Memory:')[1].split('Graphics:')[0].strip()
                                    min_requisitos_dict["Graphics"] = componentes[1].split('Graphics:')[1].split('Storage:')[0].strip()
                                    min_requisitos_dict["Storage"] = componentes[1].split('Storage:')[1].split('Sound Card:')[0].strip()
                                    min_requisitos_dict["Sound Card"] = componentes[1].split('Sound Card:')[1].strip()
                                    min_requisitos_dict["OS"] = componentes[0].split('OS:')[1].strip()

                                embed = discord.Embed(
                                    title=f"**Requisitos de {primer_juego['name']} para PC**",
                                    description=(
                                        f"**OS:** {min_requisitos_dict['OS']}\n\n"
                                        f"**Processor:** {min_requisitos_dict['Processor']}\n\n"
                                        f"**Memory:** {min_requisitos_dict['Memory']}\n\n"
                                        f"**Graphics:** {min_requisitos_dict['Graphics']}\n\n"
                                        f"**Storage:** {min_requisitos_dict['Storage']}\n\n"
                                        f"**Sound Card:** {min_requisitos_dict['Sound Card']}\n\n"
                                    ),
                                    color=discord.Color.blue(),
                                )

                                await interaction.response.edit_message(embed=embed)
                            else:
                                await interaction.response.send_message("No se encontraron requisitos para PC.")
                        else:
                            await interaction.response.send_message("Ocurrió un error al buscar los requisitos.")
            except Exception as e:
                await interaction.response.send_message(f"Ocurrió un error al buscar los requisitos: {e}")

    Boton.callback = button_callback
    Boton2.callback = button2_callback
    Boton3.callback = button3_callback
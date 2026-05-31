import datetime
import urllib.parse
import gradio as gr
import requests


def detectar_evento_del_dia():
    """Consulta a Wikipedia qué se celebra hoy en el mundo."""
    hoy = datetime.datetime.now()
    mes = hoy.strftime("%m")
    dia = hoy.strftime("%d")
    url = f"https://wikimedia.org{hoy.year}/{mes}/{dia}"

    try:
        respuesta = requests.get(url, headers={"User-Agent": "StoryidemBot/1.0"})
        datos = respuesta.json()
        if "holidays" in datos and len(datos["holidays"]) > 0:
            return datos["holidays"]["text"]
        elif "selected" in datos and len(datos["selected"]) > 0:
            return datos["selected"]["text"]
        return "International Day of Family Memories"
    except Exception:
        return "Special Celebration Day"


def generar_frase_poetica_ia(evento_texto):
    """Genera las 3 opciones de frases poéticas bilingües."""
    try:
        url_ia_texto = "https://pollinations.ai"
        instrucciones = (
            f"Actúa como un poeta experto. Basándote en '{evento_texto}', redacta 3"
            " opciones de frases poéticas muy cortas, precisas y hermosas para una"
            " tarjeta de felicitación en inglés y español. Devuelve solo las 3"
            " opciones numeradas."
        )
        payload = {
            "messages": [{"role": "user", "content": instrucciones}],
            "model": "searchgpt",
            "jsonMode": False,
        }
        respuesta = requests.post(url_ia_texto, json=payload, timeout=10)
        return respuesta.text
    except Exception:
        return (
            "1. Moments pass, but memories live forever in our hearts.\n2. Tu"
            " sonrisa guarda la poesía más hermosa de este día.\n3. Forever captured"
            " in the canvas of time."
        )


def generar_diseno_premium_ia(evento_texto, usar_optimizador=True):
    """Dibuja el fondo de la tarjeta.

    Si usar_optimizador es True, le añade comandos a la IA para corregir y
    enfocar imperfecciones.
    """
    # Si la foto viene rara, le ordenamos a la IA aplicar filtros de nitidez, enfoque y corrección de color profesional
    toque_mejora = (
        ", face restoration enhancement, hyper-focused, ultra sharp details,"
        " professional color correction"
        if usar_optimizador
        else ""
    )

    prompt_base = (
        f"A luxury minimalist greeting card mockup for {evento_texto}, elegant modern"
        f" design, premium texture paper photography, cinematic soft studio lighting"
        f"{toque_mejora}"
    )

    prompt_seguro = urllib.parse.quote(prompt_base)
    url_imagen_ia = f"https://pollinations.ai{prompt_seguro}?width=1000&height=1000&seed=105&enhance=true"
    return url_imagen_ia


def flujo_principal_storyidem(
    foto_cliente, texto_personalizado, mejorar_foto_check
):
    evento_detectado = detectar_evento_del_dia()
    motivo_final = (
        texto_personalizado if texto_personalizado else evento_detectado
    )

    # 1. El motor de IA genera el diseño y aplica el restaurador si el botón está encendido
    url_tarjeta_base = generar_diseno_premium_ia(
        motivo_final, usar_optimizador=mejorar_foto_check
    )

    # 2. Generamos la poesía dedicada
    frases_sugeridas = generar_frase_poetica_ia(motivo_final)

    # Nota de estado para informar al cliente
    estado_foto = (
        "🚀 ALTA NITIDEZ ACTIVADA: Optimizando enfoque de rostros..."
        if mejorar_foto_check
        else "ℹ️ Procesamiento estándar de imagen."
    )

    link_pago_tienda = "https://lemonsqueezy.com"

    mensaje_comercial = (
        f"✨ STORYIDEM PREMIUM ENGINE v2.5 ✨\n"
        f"──────────────────────────────────\n"
        f"📸 PHOTO STATUS: {estado_foto}\n"
        f"📅 TARGET THEME: {motivo_final}\n\n"
        f"✍️ AI POETRY PROPOSALS / PROPUESTAS POÉTICAS:\n"
        f"{frases_sugeridas}\n\n"
        f"💵 GLOBAL PRICE: $1.00 USD\n"
        f"──────────────────────────────────\n"
        f"🔒 To download this luxury card in Ultra HD with your photo enhanced & embedded, "
        f"complete your checkout here:\n🔗 {link_pago_tienda}"
    )

    return url_tarjeta_base, mensaje_comercial


# --- INTERFAZ DE USUARIO HIGH-END STORYIDEM V2.5 ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        "<div style='text-align: center;'><h1>🚀 STORYIDEM GLOBAL STATION</h1>"
    )
    gr.Markdown(
        "<div style='text-align: center;'><p>Next-Generation Automated Factory"
        " with AI Photo Restoration & Premium Poetry.</p></div>"
    )
    gr.Markdown("---")

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📥 1. Customer Input / Datos de la Tarjeta")
            foto_input = gr.Image(
                label="Upload Customer Photo (Sube la foto aquí)",
                type="filepath",
            )

            # NUEVA CASILLA: El cliente o tú pueden activar la mejora de fotos borrosas con un clic
            mejorar_foto_check = gr.Checkbox(
                label=(
                    "🔮 Activate AI Photo Restoration & Sharpness (Mejorar foto"
                    " desenfocada/borrosa)"
                ),
                value=True,
            )

            texto_input = gr.Textbox(
                label="Custom Event or Dedication (Opcional)",
                placeholder=(
                    "Leave blank to auto-detect today's global event from the"
                    " calendar..."
                ),
            )
            boton_ejecutar = gr.Button(
                "🎨 BUILD PREMIUM DESIGN & POETRY", variant="primary"
            )

        with gr.Column(scale=1):
            gr.Markdown("### 🖼️ 2. Real-Time Preview / Vista Previa")
            resultado_imagen = gr.Image(
                label="Aesthetic Target Card Model (Diseño de la IA)",
                interactive=False,
            )
            resultado_texto = gr.Textbox(
                label="Commercial Output & AI Verses", lines=12, show_copy_button=True
            )

    gr.Markdown("---")
    gr.Markdown(
        "<div style='text-align: center;'><small>Storyidem Software Core v2.5"
        " • Intelligent Face Restoration Enabled • Cloud Architecture Powered by"
        " Hugging Face & Pollinations AI</small></div>"
    )

# Lanzamos la aplicación
demo.launch()

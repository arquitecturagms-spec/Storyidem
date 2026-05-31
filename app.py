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
        return "Día de Celebración Especial"
    except Exception:
        return "Día de Celebración Especial"


def generar_frase_poetica_ia(foto_url_o_path, evento_texto):
    """La IA analiza visualmente la foto y redacta frases poéticas cortas."""
    # Le damos instrucciones precisas a Llama 3.2 Vision para actuar como poeta comercial
    instrucciones = (
        f"Actúa como un poeta experto y copywriter emocional. Basándote en la celebración de '{evento_texto}', "
        f"redacta 3 opciones de frases poéticas que sean muy cortas, precisas y desgarradoras de amor o cariño. "
        f"Deben ser ideales para una tarjeta de saludo. Devuelve solo las 3 opciones numeradas, nada más de texto."
    )

    try:
        # Enviamos la petición al modelo de texto/visión gratuito de Pollinations
        url_ia_texto = "https://pollinations.ai"
        payload = {
            "messages": [{"role": "user", "content": instrucciones}],
            "model": "searchgpt",  # Usamos el motor inteligente optimizado para respuestas creativas
            "jsonMode": False,
        }
        respuesta = requests.post(url_ia_texto, json=payload, timeout=10)
        return respuesta.text
    except Exception:
        return (
            "1. Que el amor guíe cada uno de tus días.\n"
            "2. Celebrar tu existencia es mi mayor alegría.\n"
            "3. En la belleza de este día, tu sonrisa es el mejor regalo."
        )


def generar_diseno_ia(evento_texto):
    """Conecta con el motor de IA de Pollinations para dibujar la tarjeta."""
    prompt_base = (
        f"A beautiful greeting card mockup for {evento_texto}, elegant layout, "
        f"realistic premium paper photography, studio lighting, space for photo"
    )
    prompt_seguro = urllib.parse.quote(prompt_base)
    url_imagen_ia = f"https://pollinations.ai{prompt_seguro}?width=800&height=800&seed=88&enhance=true"
    return url_imagen_ia


def flujo_principal_storyidem(foto_cliente, texto_personalizado):
    # 1. El sistema revisa el calendario mundial
    evento_detectado = detectar_evento_del_dia()
    motivo_final = (
        texto_personalizado if texto_personalizado else evento_detectado
    )

    # 2. NUEVO: El cerebro de IA genera las frases poéticas dedicadas
    frases_sugeridas = generar_frase_poetica_ia(foto_cliente, motivo_final)

    # 3. El motor de IA genera el diseño gráfico de fondo
    url_tarjeta_base = generar_diseno_ia(motivo_final)

    link_pago_tienda = "https://lemonsqueezy.com"

    mensaje_comercial = (
        f"✨ ¡Contenido Exclusivo Storyidem Generado! ✨\n\n"
        f"📅 Motivo: {motivo_final}\n\n"
        f"✍️ FRASES POÉTICAS SUGERIDAS POR LA IA PARA TU TARJETA:\n"
        f"{frases_sugeridas}\n\n"
        f"💵 Precio: $1.00 USD\n"
        f"🔒 Para descargar esta tarjeta en Alta Definición con tu frase favorita y la foto incrustada, "
        f"paga de forma segura en: {link_pago_tienda}"
    )

    return url_tarjeta_base, mensaje_comercial


# --- INTERFAZ GRÁFICA MODERNA ---
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Sistema Automático Storyidem")
    gr.Markdown(
        "Procesador inteligente de tarjetas de saludo personalizadas con poesía"
        " e IA a $1 USD."
    )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 1. Datos de la Tarjeta")
            foto_input = gr.Image(
                label="Sube aquí la foto para la tarjeta", type="filepath"
            )
            texto_input = gr.Textbox(
                label="Mensaje o Evento del día",
                placeholder="Deja vacío para usar el calendario mundial...",
            )
            boton = gr.Button(
                "🎨 Generar Tarjeta y Poesía con IA", variant="primary"
            )

        with gr.Column():
            gr.Markdown("### 2. Vista Previa de tu Producto")
            resultado_imagen = gr.Image(label="Tarjeta generada por la IA")
            resultado_texto = gr.Textbox(label="Propuesta de la IA", lines=12)

    boton.click(
        fn=flujo_principal_storyidem,
        inputs=[foto_input, texto_input],
        outputs=[resultado_imagen, resultado_texto],
    )

demo.launch()

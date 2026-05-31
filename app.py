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
            return datos["holidays"][0]["text"]
        elif "selected" in datos and len(datos["selected"]) > 0:
            return datos["selected"][0]["text"]
        return "International Celebration Day"
    except Exception:
        return "Special Celebration Day"


def generar_diseno_ia(evento_texto):
    """Conecta con el motor de IA de Pollinations para dibujar la tarjeta."""
    # Traducimos visualmente el evento en un prompt profesional de diseño para la IA
    prompt_base = (
        f"A premium greeting card mockup for {evento_texto}, elegant layout, "
        f"realistic texture, studio lighting, photorealistic, place for custom photo"
    )

    # Codificamos el texto para que internet lo entienda sin problemas de espacios
    prompt_seguro = urllib.parse.quote(prompt_base)

    # Generamos el enlace de la imagen mágica en tiempo real (usamos una semilla aleatoria para variar)
    url_imagen_ia = f"https://pollinations.ai{prompt_seguro}?width=800&height=800&seed=45&enhance=true"
    return url_imagen_ia


def flujo_principal_storyidem(foto_cliente, texto_personalizado):
    # 1. El sistema escanea el calendario
    evento_detectado = detectar_evento_del_dia()

    # Si el cliente escribe algo propio, se usa eso; si no, el evento automático del día
    motivo_final = (
        texto_personalizado if texto_personalizado else evento_detectado
    )

    # 2. El motor de IA genera el diseño gráfico de fondo en segundos
    url_tarjeta_base = generar_diseno_ia(motivo_final)

    # Enlace de pago simulado (se cambiará por tu link real de Lemon Squeezy en la Fase 3)
    link_pago_tienda = "https://lemonsqueezy.com"

    mensaje_comercial = (
        f"✨ ¡Diseño exclusivo de Storyidem generado con éxito para ti! ✨\n\n"
        f"📅 Motivo procesado: {motivo_final}\n"
        f"💵 Precio: $1.00 USD (Conversión automática a tu moneda local)\n\n"
        f"🔒 Para descargar esta tarjeta en Alta Definición (HD) con tu fotografía incrustada, "
        f"haz clic en nuestro enlace seguro de pago:\n"
        f"🔗 {link_pago_tienda}\n\n"
        f"Al completar el pago, recibirás el archivo final listo para imprimir directamente en tu correo electrónico."
    )

    # Retornamos el mensaje de texto y el enlace de la imagen generada por la IA
    return mensaje_comercial, url_tarjeta_base


# --- INTERFAZ GRÁFICA DE LA TIENDA GLOBAL STORYIDEM ---
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🚀 Fábrica Digital Automatizada Storyidem")
    gr.Markdown(
        "Bienvenido al motor inteligente de tarjetas con fotos personalizadas a"
        " $1 USD a nivel mundial."
    )

    with gr.Row():
        with gr.Column():
            gr.Markdown("### 1. Datos de tu Tarjeta")
            foto_input = gr.Image(
                label="Sube aquí tu fotografía favorita", type="filepath"
            )
            texto_input = gr.Textbox(
                label="Mensaje o dedicatoria (Opcional)",
                placeholder=(
                    "Deja vacío para usar la conmemoración mundial automática de"
                    " hoy..."
                ),
            )
            boton_enviar = gr.Button(
                "🎨 Generar Diseño Exclusivo con IA", variant="primary"
            )

        with gr.Column():
            gr.Markdown("### 2. Vista Previa de tu Producto")
            resultado_imagen = gr.Image(
                label="Diseño sugerido por la IA de Storyidem"
            )
            resultado_texto = gr.Textbox(
                label="Instrucciones de Compra", lines=8
            )

    # Conectamos las acciones del botón
    boton_enviar.click(
        fn=flujo_principal_storyidem,
        inputs=[foto_input, texto_input],
        outputs=[resultado_texto, resultado_imagen],
    )

demo.launch()

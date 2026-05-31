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
        return "Day of International Celebration"
    except Exception:
        return "Special Celebration Day"


def generar_diseno_ia(evento_texto):
    """Conecta con el motor de IA de Pollinations para dibujar la tarjeta."""
    # Creamos un prompt artístico para la IA basado en la fecha
    prompt_base = (
        f"A beautiful greeting card mockup for {evento_texto}, elegant layout, "
        f"realistic premium paper photography, studio lighting, space for photo"
    )
    # Codificamos el texto para internet
    prompt_seguro = urllib.parse.quote(prompt_base)
    # Enlace de la imagen mágica en tiempo real
    url_imagen_ia = f"https://pollinations.ai{prompt_seguro}?width=800&height=800&seed=99&enhance=true"
    return url_imagen_ia


def flujo_principal_storyidem(foto_cliente, texto_personalizado):
    # 1. El sistema revisa el calendario mundial
    evento_detectado = detectar_evento_del_dia()

    # Si el usuario escribe algo, se usa eso; si no, el evento de hoy
    motivo_final = (
        texto_personalizado if texto_personalizado else evento_detectado
    )

    # 2. El motor de IA genera el diseño gráfico de fondo en segundos
    url_tarjeta_base = generar_diseno_ia(motivo_final)

    # Enlace provisional de tu tienda Lemon Squeezy
    link_pago_tienda = "https://lemonsqueezy.com"

    mensaje_comercial = (
        f"✨ ¡Diseño Exclusivo Storyidem Generado! ✨\n\n"
        f"📅 Motivo: {motivo_final}\n"
        f"💵 Precio: $1.00 USD\n\n"
        f"🔒 Para descargar esta tarjeta en Alta Definición con tu foto incrustada, "
        f"paga de forma segura en: {link_pago_tienda}"
    )

    return url_tarjeta_base, mensaje_comercial


# --- INTERFAZ GRÁFICA MODERNA ---
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Sistema Automático Storyidem")
    gr.Markdown(
        "Procesador inteligente de tarjetas de saludo personalizadas a $1 USD."
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
                "🎨 Generar Tarjeta de Muestra con IA", variant="primary"
            )

        with gr.Column():
            gr.Markdown("### 2. Vista Previa de tu Producto")
            resultado_imagen = gr.Image(label="Tarjeta generada por la IA")
            resultado_texto = gr.Textbox(label="Estado del Sistema", lines=5)

    boton.click(
        fn=flujo_principal_storyidem,
        inputs=[foto_input, texto_input],
        outputs=[resultado_imagen, resultado_texto],
    )

demo.launch()

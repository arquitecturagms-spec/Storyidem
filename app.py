import datetime
import gradio as gr
import requests


def detectar_evento_del_dia():
    """Este es el cerebro del calendario.

    Consulta a Wikipedia qué se celebra hoy en el mundo.
    """
    hoy = datetime.datetime.now()
    mes = hoy.strftime("%m")
    dia = hoy.strftime("%d")

    # Consultamos la base de datos global de Wikipedia para la fecha de hoy
    url = f"https://wikimedia.org{hoy.year}/{mes}/{dia}"

    try:
        respuesta = requests.get(url, headers={"User-Agent": "StoryidemBot/1.0"})
        datos = respuesta.json()

        # Buscamos un evento importante o día festivo registrado para hoy
        if "holidays" in datos and len(datos["holidays"]) > 0:
            # Tomamos la primera conmemoración oficial mundial del día
            evento_nombre = datos["holidays"][0]["text"]
            return f"📅 EVENTO DETECTADO HOY: {evento_nombre}"

        elif "selected" in datos and len(datos["selected"]) > 0:
            # Si no hay festivo, tomamos un hecho histórico importante del día
            evento_nombre = datos["selected"][0]["text"]
            return f"⏳ ANIVERSARIO HISTÓRICO HOY: {evento_nombre}"

        return "🌍 Hoy es un día de celebraciones generales en el mundo."
    except Exception:
        return "📅 Conectado al calendario global de Storyidem (Modo General)."


def procesar_tarjeta_storyidem(foto, texto_manual):
    # El sistema revisa automáticamente qué fecha es hoy en el mundo
    evento_actual = detectar_evento_del_dia()

    # Si el usuario escribe algo personalizado, usamos eso, si no, usamos el evento del día
    motivo_final = texto_manual if texto_manual else evento_actual

    return (
        f"¡Máquina Storyidem Activa!\n\n"
        f"1. Motivo del diseño: {motivo_final}\n"
        f"2. Estado: Esperando integración del motor de imagen para fusionar la foto."
    )


# --- INTERFAZ VISUAL DE STORYIDEM ---
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Sistema Inteligente Storyidem")
    gr.Markdown(
        "Esta máquina detecta eventos mundiales automáticamente y procesa tarjetas por $1"
        " USD."
    )

    # Botón mágico para que tú o el cliente vean qué fecha detecta el sistema HOY
    botón_calendario = gr.Button("🔍 Probar Detector de Calendario Mundial")
    texto_calendario = gr.Text(label="Resultado del escáner global")
    botón_calendario.click(fn=detectar_evento_del_dia, outputs=texto_calendario)

    gr.Markdown("---")
    gr.Markdown("### Área de simulación de compra ($1 USD)")

    with gr.Row():
        foto_input = gr.Image(label="Foto que sube el cliente")
        texto_input = gr.Textbox(
            label="Texto personalizado (O déjalo vacío para usar el evento del día)"
        )

    boton_procesar = gr.Button("Generar Tarjeta")
    salida_estado = gr.Text(label="Estado del Motor Storyidem")

    boton_procesar.click(
        fn=procesar_tarjeta_storyidem,
        inputs=[foto_input, texto_input],
        outputs=salida_estado,
    )

demo.launch()

import gradio as gr

def procesar_tarjeta(foto, texto_saludo):
    # El motor de IA de Storyidem unirá la foto y el texto aquí
    return "¡Diseño procesado con éxito por el motor de Storyidem!"

# Interfaz visual básica de tu fábrica digital
with gr.Blocks() as demo:
    gr.Markdown("# 🚀 Sistema Automático Storyidem")
    gr.Markdown("Procesador inteligente de tarjetas de saludo personalizadas a $1 USD.")
    
    with gr.Row():
        foto_input = gr.Image(label="Foto enviada por el cliente")
        texto_input = gr.Textbox(label="Mensaje o Evento del día")
    
    boton = gr.Button("Generar Tarjeta de Muestra")
    salida = gr.Text(label="Estado del Sistema")
    
    boton.click(fn=procesar_tarjeta, inputs=[foto_input, texto_input], outputs=salida)

demo.launch()

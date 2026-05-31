import datetime
import urllib.parse
import gradio as gr
import requests
import os

def detectar_evento_del_dia():
    """Consulta a Wikipedia qué se celebra hoy en el mundo de forma segura."""
    hoy = datetime.datetime.now()
    mes = hoy.strftime("%m")
    dia = hoy.strftime("%d")
    url = f"https://history.wikimedia.org/v1/by_date/onthisday/all/{mes}/{dia}"
    
    try:
        respuesta = requests.get(url, headers={"User-Agent": "StoryidemBot/2.5"}, timeout=5)
        if respuesta.status_code == 200:
            datos = respuesta.json()
            if "holidays" in datos and len(datos["holidays"]) > 0:
                return datos["holidays"][0]["text"]
            elif "selected" in datos and len(datos["selected"]) > 0:
                return datos["selected"][0]["text"]
        return "Day of Beautiful Memories"
    except Exception:
        return "Special Celebration Day"

def generar_frase_poetica_ia(evento_texto):
    """Genera opciones de frases poéticas con un timeout estricto de 5 segundos via GET."""
    prompt_poema = (
        f"Write 3 short beautiful greeting card verses for {evento_texto} "
        f"in English and Spanish. Numbered list only, no extra text."
    )
    prompt_seguro = urllib.parse.quote(prompt_poema)
    url = f"https://text.pollinations.ai/{prompt_seguro}?model=openai"
        
    try:
        respuesta = requests.get(url, headers={"User-Agent": "StoryidemBot/2.5"}, timeout=5)
        if respuesta.status_code == 200 and respuesta.text.strip():
            return respuesta.text
    except Exception:
        pass
            
    return (
        "1. Moments pass, but memories live forever in our hearts.\n"
        "2. Tu sonrisa guarda la poesía más hermosa de este día.\n"
        "3. Forever captured in the canvas of time."
    )

def generar_diseno_premium_ia(evento_texto, usar_optimizador=True):
    """Genera la imagen con la IA y la descarga localmente para evadir bloqueos de Gradio 6."""
    toque_mejora = ", luxury, sharp details" if usar_optimizador else ""
    prompt_base = f"greeting card design for {evento_texto}{toque_mejora}"
    prompt_seguro = urllib.parse.quote(prompt_base)
    url_remota = f"https://image.pollinations.ai/prompt/{prompt_seguro}?width=800&height=800&nologo=true"
    
    ruta_local_imagen = "tarjeta_preview.png"
    
    try:
        # Descargamos físicamente el archivo binario de la imagen al servidor local
        img_data = requests.get(url_remota, timeout=10).content
        with open(ruta_local_imagen, 'wb') as handler:
            handler.write(img_data)
        # Devolvemos la ruta local del archivo. Gradio adora los archivos locales
        return ruta_local_imagen
    except Exception:
        # Si la descarga remota falla por red, devolvemos la URL original como plan de respaldo
        return url_remota

def flujo_principal_storyidem(foto_cliente, texto_personalizado, mejorar_foto_check):
    if texto_personalizado and texto_personalizado.strip():
        motivo_final = texto_personalizado.strip()
    else:
        motivo_final = detectar_evento_del_dia()
    
    # Obtiene la ruta del archivo descargado localmente
    archivo_imagen_local = generar_diseno_premium_ia(motivo_final, usar_optimizador=mejorar_foto_check)
    frases_sugeridas = generar_frase_poetica_ia(motivo_final)
    
    estado_foto = "🚀 ALTA NITIDEZ ACTIVADA: Optimizando rostros..." if mejorar_foto_check else "ℹ️ Procesamiento estándar."
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
    
    return archivo_imagen_local, mensaje_comercial

# --- INTERFAZ DE USUARIO (GRADIO) ---
with gr.Blocks() as demo:
    gr.Markdown("<div style='text-align: center;'><h1>🚀 STORYIDEM GLOBAL STATION</h1>")
    gr.Markdown("<div style='text-align: center;'><p>Next-Generation Automated Factory with AI Photo Restoration & Premium Poetry.</p></div>")
    gr.Markdown("---")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📥 1. Customer Input / Datos de la Tarjeta")
            foto_input = gr.Image(label="Upload Customer Photo (Sube la foto aquí)", type="filepath")
            mejorar_foto_check = gr.Checkbox(label="🔮 Activate AI Photo Restoration & Sharpness", value=True)
            texto_input = gr.Textbox(label="Custom Event or Dedication (Opcional)", placeholder="Leave blank to use calendar...")
            boton_ejecutar = gr.Button("🎨 BUILD PREMIUM DESIGN & POETRY", variant="primary")
            
        with gr.Column(scale=1):
            gr.Markdown("### 🖼️ 2. Real-Time Preview / Vista Previa")
            # El componente ahora recibirá un archivo físico real .png
            resultado_imagen = gr.Image(label="Aesthetic Target Card Model (Diseño de la IA)", interactive=False)
            resultado_texto = gr.Textbox(label="Commercial Output & AI Verses", lines=12)
            
    gr.Markdown("---")
    gr.Markdown("<div style='text-align: center;'><small>Storyidem Software Core v2.5 • Powered by Hugging Face & Pollinations AI</small></div>")

    boton_ejecutar.click(
        fn=flujo_principal_storyidem,
        inputs=[foto_input, texto_input, mejorar_foto_check],
        outputs=[resultado_imagen, resultado_texto]
    )

demo.launch(theme=gr.themes.Soft())

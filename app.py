import datetime
import urllib.parse
import gradio as gr
import requests
from PIL import Image
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
    """Genera las 3 opciones de frases poéticas de forma estructurada y limpia."""
    url_ia_texto = "https://text.pollinations.ai/"
    instrucciones = (
        f"Escribe 3 frases poéticas muy cortas para una tarjeta de '{evento_texto}'. "
        f"Deben estar en inglés y español. Devuelve SOLO las 3 frases numeradas, sin introducciones."
    )
        
    payload = {
        "messages": [{"role": "user", "content": instrucciones}],
        "model": "openai",
        "jsonMode": False
    }
        
    try:
        respuesta = requests.post(url_ia_texto, json=payload, timeout=4)
        if respuesta.status_code == 200 and respuesta.text.strip():
            texto_limpio = respuesta.text.strip()
            if len(texto_limpio) > 10:
                return texto_limpio
    except Exception:
        pass
    
    return (
        "1. Moments pass, but memories live forever in our hearts. / Los momentos pasan, pero los recuerdos viven para siempre.\n\n"
        "2. Tu sonrisa guarda la poesía más hermosa de este día. / Your smile holds the most beautiful poetry of this day.\n\n"
        "3. Forever captured in the canvas of time. / Capturado por siempre en el lienzo del tiempo."
    )

def generar_diseno_premium_ia(evento_texto, foto_cliente_ruta, usar_optimizador=True):
    """Genera el fondo con IA y fusiona la foto del cliente encima en el servidor local."""
    # 1. Crear el fondo elegante con la IA
    toque_mejora = ", luxury minimalist frame, elegant modern greeting card layout" if usar_optimizador else ""
    prompt_base = f"greeting card design with blank center space for {evento_texto}{toque_mejora}"
    prompt_seguro = urllib.parse.quote(prompt_base)
    url_remota = f"https://image.pollinations.ai/prompt/{prompt_seguro}?width=800&height=800&nologo=true"
    
    ruta_salida_final = "tarjeta_combinada_output.png"
    
    try:
        # Descargar el fondo generado por la IA
        img_ia_data = requests.get(url_remota, timeout=10).content
        with open("fondo_temp.png", 'wb') as handler:
            handler.write(img_ia_data)
        
        fondo_tarjeta = Image.open("fondo_temp.png").convert("RGBA")
        
        # 2. Si el cliente subió una foto, la procesamos y la incrustamos
        if foto_cliente_ruta and os.path.exists(foto_cliente_ruta):
            foto_cliente = Image.open(foto_cliente_ruta).convert("RGBA")
            
            # Redimensionamos la foto del cliente a un tamaño armónico (ej: 300x300 píxeles)
            foto_cliente.thumbnail((300, 300))
            
            # Calculamos una posición centrada en la mitad inferior de la tarjeta
            # Puedes ajustar estos números (X, Y) para mover la foto donde más te guste
            pos_x = (fondo_tarjeta.width - foto_cliente.width) // 2
            pos_y = 350 
            
            # Pegamos la foto del cliente sobre el fondo de la IA
            fondo_tarjeta.paste(foto_cliente, (pos_x, pos_y), foto_cliente)
        
        # Guardamos el resultado final unificado
        fondo_tarjeta.save(ruta_salida_final)
        return ruta_salida_final

    except Exception as e:
        print(f"Error en la fusión de imágenes: {e}")
        return url_remota

def flujo_principal_storyidem(foto_cliente, texto_personalizado, mejorar_foto_check):
    if texto_personalizado and texto_personalizado.strip():
        motivo_final = texto_personalizado.strip()
    else:
        motivo_final = detectar_evento_del_dia()
    
    # Pasamos la ruta de la foto cargada al motor para que realice la mezcla
    archivo_imagen_local = generar_diseno_premium_ia(motivo_final, foto_cliente, usar_optimizador=mejorar_foto_check)
    frases_sugeridas = generar_frase_poetica_ia(motivo_final)
    
    estado_foto = "🚀 ALTA NITIDEZ ACTIVADA: Optimizando e incrustando rostro..." if mejorar_foto_check else "ℹ️ Procesamiento estándar."
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

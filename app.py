import streamlit as st
import yt_dlp
import os

# Configuración de la página web
st.set_page_config(page_title="Convertidor YouTube a MP3", page_icon="🎵", layout="centered")

# Estilos CSS para el parpadeo y la alineación de las manos
st.markdown("""
    <style>
    @keyframes parpadear {
        0% { opacity: 1; }
        50% { opacity: 0.2; }
        100% { opacity: 1; }
    }
    .hand-anim-left {
        font-size: 32px;
        animation: parpadear 1s infinite;
        text-align: right;
        margin-top: -15px;
    }
    .hand-anim-right {
        font-size: 32px;
        animation: parpadear 1s infinite;
        text-align: left;
        margin-top: -15px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎵 Convertidor de YouTube a MP3")
st.write("Pega el enlace de cualquier video de YouTube para extraer y descargar su audio en formato MP3 al instante.")

# Texto guía superior
st.markdown("<div style='text-align: center; color: gray; font-style: italic; margin-bottom: 5px;'>( Pega tu enlace en la caja de abajo )</div>", unsafe_allow_html=True)

# Distribución en columnas con las manos a los costados
col_izq, col_input, col_der = st.columns([0.08, 0.84, 0.08])

with col_izq:
    st.markdown('<div class="hand-anim-left">👉</div>', unsafe_allow_html=True)

with col_input:
    url = st.text_input("Pega el enlace de YouTube aquí:", placeholder="AQUÍ PEGUE LO QUE COPIO", label_visibility="collapsed")

with col_der:
    st.markdown('<div class="hand-anim-right">👈</div>', unsafe_allow_html=True)

# Botón de conversión
if st.button("Convertir y Descargar MP3", type="primary"):
    if not url:
        st.warning("Por favor, ingresa un enlace de YouTube válido.")
    else:
        with st.spinner("Descargando y convirtiendo audio... Por favor espera."):
            try:
               opciones = {
                    'format': 'bestaudio/best',
                    'noplaylist': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': '%(title)s.%(ext)s',
                    'restrictfilenames': True,
                    'extractor_args': {'youtube': {'player_client': ['mweb', 'android']}},
                }
                
                with yt_dlp.YoutubeDL(opciones) as ydl:
                    info = ydl.extract_info(url, download=True)
                    nombre_archivo = ydl.prepare_filename(info)
                    nombre_mp3 = os.path.splitext(nombre_archivo)[0] + ".mp3"
                
                if os.path.exists(nombre_mp3):
                    st.success("¡Conversión exitosa!")
                    
                    with open(nombre_mp3, "rb") as archivo:
                        st.download_button(
                            label="📥 Haz clic aquí para descargar tu MP3",
                            data=archivo,
                            file_name=os.path.basename(nombre_mp3),
                            mime="audio/mp3"
                        )
                else:
                    st.error("No se pudo generar el archivo MP3.")
                    
            except Exception as e:
                st.error(f"Ocurrió un error durante el proceso: {str(e)}")

# Sección de Tutorial (Video Local)
st.markdown("---")
st.subheader("📺 Tutorial: ¿Cómo usar el convertidor?")
st.write("Mira el siguiente video explicativo para aprender a usar la herramienta paso a paso:")

ruta_tutorial = "tutorial.mp4"

if os.path.exists(ruta_tutorial):
    st.video(ruta_tutorial)
else:
    st.info("💡 Coloca tu archivo 'tutorial.mp4' en el repositorio de GitHub para mostrar el video tutorial aquí.")

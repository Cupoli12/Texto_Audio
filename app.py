import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# Page title and image display
st.set_page_config(page_title="Conversión de Texto a Audio", layout="centered")
st.title("Conversión de Texto a Audio")

# Display the image
image = Image.open('gato_raton.png')
st.image(image, caption="Kafka's Tale", use_column_width=True)

# Sidebar setup
with st.sidebar:
    st.header("Configuración")
    st.info("Escribe o selecciona el texto que deseas convertir en audio.", icon="🔊")

# Create 'temp' directory if not exists
if not os.path.exists("temp"):
    os.mkdir("temp")

# Display a brief fable with styling
st.subheader("Una pequeña Fábula")
st.markdown(
    """
    <div style="background-color:#f44336; padding: 10px; border-radius: 10px;">
    ¡Ay! -dijo el ratón-. El mundo se hace cada día más pequeño. Al principio era tan grande que le tenía miedo.
    Corría y corría y por cierto que me alegraba ver esos muros, a diestra y siniestra, en la distancia.
    Pero esas paredes se estrechan tan rápido que me encuentro en el último cuarto y ahí en el rincón está
    la trampa sobre la cual debo pasar. Todo lo que debes hacer es cambiar de rumbo dijo el gato... y se lo comió.
    <br><br><strong>Franz Kafka.</strong>
    </div>
    """, unsafe_allow_html=True
)

# Text input area
st.markdown("## ¿Te gustaría escucharlo? Copia el texto a continuación:")
text = st.text_area("Ingrese el texto que desea convertir a audio", height=200)

# Language selection dropdown
option_lang = st.selectbox("Selecciona el idioma del audio:", ("Español", "English"))
lg = 'es' if option_lang == "Español" else 'en'

# Text-to-speech function
def text_to_speech(text, lg):
    tts = gTTS(text, lang=lg)
    my_file_name = text[:20] if text else "audio"
    file_path = f"temp/{my_file_name}.mp3"
    tts.save(file_path)
    return file_path, text

# Convert text to audio button
if st.button("Convertir a Audio"):
    if text.strip():
        audio_path, output_text = text_to_speech(text, lg)
        audio_file = open(audio_path, "rb")
        audio_bytes = audio_file.read()
        
        st.markdown("## Tu Audio:")
        st.audio(audio_bytes, format="audio/mp3")

        # Audio download link
        with open(audio_path, "rb") as f:
            data = f.read()
            def get_binary_file_downloader_html(bin_file, file_label='File'):
                bin_str = base64.b64encode(data).decode()
                href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{os.path.basename(bin_file)}">Descargar {file_label}</a>'
                return href
            st.markdown(get_binary_file_downloader_html(audio_path, "Archivo de Audio"), unsafe_allow_html=True)
    else:
        st.warning("Por favor, ingrese un texto para convertir a audio.")

# Cleanup old files
def remove_old_files(days=1):
    mp3_files = glob.glob("temp/*.mp3")
    now = time.time()
    threshold = days * 86400  # Convert days to seconds
    for f in mp3_files:
        if os.stat(f).st_mtime < now - threshold:
            os.remove(f)

# Remove files older than one day
remove_old_files(1)


#importamos los framework a utilizar
from cProfile import label

import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO

# from streamlit import download_button

st.set_page_config(layout="wide", page_title="Eliminador de fondos de imagenes")

st.write("## Elimina el fondo de tu imagen")

st.write(
    ":dog: Sube una imagen y observa cómo se elimina mágicamente el fondo. "
    "Las imágenes de alta calidad se pueden descargar desde la barra lateral. "
    "Este código es de código abierto y está disponible [aquí](http://github.com/tyler-simons/BackgroundRemoval) en GitHub. "
    "¡Gracias especiales a la biblioteca rembg! :grin:"
)

st.sidebar.write("## Subir y descargar :gear:")

MAX_TAMAÑO_ARCHIVO = 5 * 1024 * 1024 #5MB

def arreglar_imagen(imagen_subida):
    imagen = Image.open(imagen_subida)
    col1, col2 = st.columns(2)

    col1.write("Imagen original :camera:")
    col1.image(imagen)

    sin_fondo = remove(imagen)
    col2.write("Imagen sin fondo :winking_face:")
    col2.image(sin_fondo)

#     preparar la imagen para la descarga
    buffered = BytesIO()
    sin_fondo.convert("RGB").save(buffered, format("JPEG"))
    buffered.seek(0)

    st.download_button(
        label="Descaragar Imagen Sin Fondo",
        data=buffered,
        file_name="Imagen_sin_fondo.jpg",
        mime="image/jpeg"
    )
mi_subida = st.sidebar.file_uploader("Sube una imagen", type=["png","jpg","jpeg"])

if mi_subida is not None:
    if mi_subida.size > MAX_TAMAÑO_ARCHIVO:
        st.error("El archivo subido es demasiado grande. Sube una imagen menor a 5MB")
    else:
        arreglar_imagen(mi_subida)
else:
    st.info("¡Sube una imagen para comenzar!")

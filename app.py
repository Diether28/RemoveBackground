#importamos los framework a utilizar
import streamlit as st
from rembg import remove
from PIL import Image, UnidentifiedImageError
from io import BytesIO

# Configuracion de la pagina
st.set_page_config(
    layout="wide", 
    page_title="Eliminador de fondos de imagenes"
)
st.title(" 🖼️Elimina el fondo de tu imagen")

st.write(
    ":dog: Sube una imagen y observa cómo se elimina mágicamente el fondo. "
    "Las imágenes de alta calidad se pueden descargar desde la barra lateral. "
    "Este código es de código abierto y está disponible [aquí](http://github.com/tyler-simons/BackgroundRemoval) en GitHub. "
    "¡Gracias especiales a la biblioteca rembg! :grin:"
)

# seleccion de subidas y opciones de descarga en la barra lateral
st.sidebar.write("## Subir y descargar :gear:")

# Tamaño maximo permitido
MAX_TAMAÑO_ARCHIVO = 5 * 1024 * 1024 #5MB

# Opciones para formato y nombre del archivo
formato = st.sidebar.selectbox(
    "Selecciona el formato de descarga",["PNG","JPEG"]
)
nombre_image = st.sidebar.text_input(
    "Ingrese el nombre del archivo",
    value="imagen_sin_fondo"
)

def arreglar_imagen(imagen_subida):
    try:
        # Intentar abrir con el soporte de transparencia
        imagen = Image.open(imagen_subida).convert("RGBA")
    except UnidentifiedImageError:
        st.error("Error: No se pudo abrir la imagen. Asegúrate de subir un archivo válido.")
        return
    # Mostrar la columna para comparación
    col1, col2 = st.columns(2)
    col1.write("Imagen original :camera:")
    col1.image(imagen, use_column_width=True)

    # Remover fondo
    try:
        sin_fondo = remove(imagen)
    except Exception as e:
        st.error(f"Hubo un error al procesar la imagen: {str(e)}")
        return
    
    col2.write("Imagen sin fondo ✨")
    col2.image(sin_fondo, use_column_width=True)

#     preparar la imagen para la descarga
    buffered = BytesIO()
    if formato == "JPEG":
        sin_fondo = sin_fondo.convert("RGB") 
        # Comvertir para compatibilidad con JPEG
        sin_fondo.save(
            buffered,
            format="JPEG",
            quality=90
        )
        mime_type = "image/png"
        extension = "png"

        buffered.seek(0)

        # Boton de descarga
    st.download_button(
        label="Descaragar Imagen Sin Fondo",
        data=buffered,
        file_name=f"{nombre_image}.{extension}",
        mime_type="image/jpeg"
    )

    # Subida de imagen en la barra lateral
mi_subida = st.sidebar.file_uploader("Sube una imagen (JPG,PNG,JPEG)", type=["png","jpg","jpeg"])

if mi_subida is not None:
    if mi_subida.size > MAX_TAMAÑO_ARCHIVO:
        st.error("El archivo subido es demasiado grande. Sube una imagen menor a 5MB")
    else:
        arreglar_imagen(mi_subida)
else:
    st.info("¡Sube una imagen para comenzar!")

import os
import streamlit as st

# Configuración de la página en modo ancho (wide)
st.set_page_config(
    page_title="PrimaScore | Evaluador de Opcionabilidad",
    page_icon="📈",
    layout="wide",
)

# Ruta del archivo HTML externo
html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

if os.path.exists(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_code = f.read()

    # Renderizar el HTML interactivo en Streamlit
    st.components.v1.html(html_code, height=980, scrolling=True)
else:
    st.error(
        "No se encuentra el archivo 'index.html'. Asegúrate de subirlo a GitHub junto con 'app.py'."
    )

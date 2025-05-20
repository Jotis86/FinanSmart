import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# Título de la aplicación
st.title("Prueba de Autenticación")

# Cargar configuración
try:
    with open('config.yaml', 'r') as file:
        config = yaml.load(file, SafeLoader)
    
    # Configurar autenticador
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    # Intento 1 - Usando los parámetros básicos
    st.subheader("Método 1")
    try:
        name, authentication_status, username = authenticator.login('Inicio de Sesión 1', 'main')
        st.write(f"Resultado: {name}, {authentication_status}, {username}")
    except Exception as e:
        st.error(f"Error método 1: {str(e)}")

    # Para ver el estado actual
    st.subheader("Estado de sesión actual")
    for key, value in st.session_state.items():
        st.write(f"{key}: {value}")

except Exception as e:
    st.error(f"Error general: {str(e)}") 
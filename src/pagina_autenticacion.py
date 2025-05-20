import streamlit as st
import streamlit_authenticator as stauth
import yaml
import os
from usuarios import cargar_configuracion, crear_usuario, crear_estructura_archivos_usuario, inicializar_sistema
from verificar_config import inicializar_config

def mostrar_pagina_registro():
    """
    Muestra la página para registrar nuevos usuarios
    """
    st.title("Registro de Usuario")
    
    with st.form("registro_form"):
        username = st.text_input("Nombre de usuario", placeholder="usuario123")
        name = st.text_input("Nombre completo", placeholder="Juan Pérez")
        email = st.text_input("Correo electrónico", placeholder="ejemplo@correo.com")
        password = st.text_input("Contraseña", type="password")
        password_confirm = st.text_input("Confirmar contraseña", type="password")
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit_button = st.form_submit_button("Registrarse")
        
        if submit_button:
            if not username or not name or not email or not password:
                st.error("Por favor, completa todos los campos.")
            elif password != password_confirm:
                st.error("Las contraseñas no coinciden.")
            else:
                # Crear el usuario
                success, message = crear_usuario(username, name, email, password)
                if success:
                    # Crear la estructura de archivos para el usuario
                    crear_estructura_archivos_usuario(username)
                    st.success(message)
                    st.success("Ya puedes iniciar sesión con tus credenciales.")
                    st.session_state.mostrar_registro = False
                else:
                    st.error(message)

def autenticar_usuario():
    """
    Maneja la autenticación de usuarios
    """
    # Primero verificamos la configuración
    inicializar_config()
    
    # Inicializar el sistema si es necesario
    inicializar_sistema()
    
    # Cargar la configuración de usuarios
    config = cargar_configuracion()
    
    # Configurar el autenticador
    try:
        authenticator = stauth.Authenticate(
            config['credentials'],
            config['cookie']['name'],
            config['cookie']['key'],
            config['cookie']['expiry_days'],
            config.get('preauthorized', {'emails': []})
        )
        
        # Mostrar la página de inicio de sesión
        name, authentication_status, username = authenticator.login('Inicio de Sesión', 'main')
    except Exception as e:
        st.error(f"Error en autenticación: {str(e)}")
        return None, None
    
    # Guardar el estado de autenticación y el nombre de usuario en session_state
    st.session_state.authentication_status = authentication_status
    st.session_state.name = name
    st.session_state.username = username
    
    # Determinar qué mostrar según el estado de autenticación
    if authentication_status is False:
        st.error('Usuario o contraseña incorrectos')
        
        # Opción para registrarse
        if 'mostrar_registro' not in st.session_state:
            st.session_state.mostrar_registro = False
            
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if not st.session_state.mostrar_registro:
                if st.button("¿No tienes cuenta? Regístrate"):
                    st.session_state.mostrar_registro = True
            else:
                if st.button("Volver al inicio de sesión"):
                    st.session_state.mostrar_registro = False
        
        if st.session_state.mostrar_registro:
            mostrar_pagina_registro()
            
    elif authentication_status is None:
        st.warning('Por favor ingresa tu usuario y contraseña')
        
        # Opción para registrarse
        if 'mostrar_registro' not in st.session_state:
            st.session_state.mostrar_registro = False
            
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if not st.session_state.mostrar_registro:
                if st.button("¿No tienes cuenta? Regístrate"):
                    st.session_state.mostrar_registro = True
            else:
                if st.button("Volver al inicio de sesión"):
                    st.session_state.mostrar_registro = False
        
        if st.session_state.mostrar_registro:
            mostrar_pagina_registro()
    
    return authenticator, authentication_status 
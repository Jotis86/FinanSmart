import streamlit as st
import yaml
import os
import bcrypt
from yaml.loader import SafeLoader
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

def verificar_password(password, hashed_password):
    """
    Verifica si la contraseña es correcta
    """
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def autenticar_usuario():
    """
    Maneja la autenticación de usuarios con un sistema simplificado
    """
    # Primero verificamos la configuración
    inicializar_config()
    
    # Inicializar el sistema si es necesario
    inicializar_sistema()
    
    # Cargar la configuración de usuarios
    config = cargar_configuracion()
    
    # Variables para devolver
    authenticator = None
    authentication_status = None
    
    # Inicializar variables de sesión si no existen
    if 'authentication_status' not in st.session_state:
        st.session_state['authentication_status'] = None
    
    if 'username' not in st.session_state:
        st.session_state['username'] = None
        
    if 'name' not in st.session_state:
        st.session_state['name'] = None
    
    # Si ya está autenticado, no hacer nada más
    if st.session_state['authentication_status'] == True:
        return None, True
    
    # Mostrar formulario de login
    st.title("Iniciar Sesión")
    
    with st.form("login_form"):
        username = st.text_input("Usuario")
        password = st.text_input("Contraseña", type="password")
        submit = st.form_submit_button("Iniciar Sesión")
    
    if submit:
        if username in config['credentials']['usernames']:
            # Verificar contraseña
            user_data = config['credentials']['usernames'][username]
            stored_password = user_data['password']
            
            if verificar_password(password, stored_password):
                # Autenticación exitosa
                st.session_state['authentication_status'] = True
                st.session_state['username'] = username
                st.session_state['name'] = user_data['name']
                authentication_status = True
                st.rerun()
            else:
                # Contraseña incorrecta
                st.session_state['authentication_status'] = False
                authentication_status = False
                st.error("Usuario o contraseña incorrectos")
        else:
            # Usuario no existe
            st.session_state['authentication_status'] = False
            authentication_status = False
            st.error("Usuario o contraseña incorrectos")
    
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
    
    # Devolver valores para compatibilidad
    return None, st.session_state['authentication_status'] 
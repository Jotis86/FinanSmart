import yaml
import os
import streamlit_authenticator as stauth
import pandas as pd
from yaml.loader import SafeLoader

# Ruta del archivo de configuración de usuarios
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')

def inicializar_usuarios():
    """
    Inicializa el archivo de configuración con usuarios por defecto si no existe
    """
    if not os.path.exists(CONFIG_PATH):
        # Configuración inicial con un usuario administrador
        config = {
            'credentials': {
                'usernames': {
                    'admin': {
                        'name': 'Administrador',
                        'email': 'admin@example.com',
                        'password': stauth.Hasher(['admin']).generate()[0]
                    }
                }
            },
            'cookie': {
                'expiry_days': 30,
                'key': 'finansmart_auth',
                'name': 'finansmart_cookie'
            },
            'preauthorized': {
                'emails': []
            }
        }
        
        with open(CONFIG_PATH, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)

def cargar_configuracion():
    """
    Carga la configuración de usuarios desde el archivo YAML
    """
    with open(CONFIG_PATH, 'r') as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def guardar_configuracion(config):
    """
    Guarda la configuración de usuarios en el archivo YAML
    """
    with open(CONFIG_PATH, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def crear_usuario(username, name, email, password):
    """
    Crea un nuevo usuario en el sistema
    """
    config = cargar_configuracion()
    
    # Verificar si el usuario ya existe
    if username in config['credentials']['usernames']:
        return False, "El nombre de usuario ya existe"
    
    # Añadir el nuevo usuario
    config['credentials']['usernames'][username] = {
        'name': name,
        'email': email,
        'password': stauth.Hasher([password]).generate()[0]
    }
    
    guardar_configuracion(config)
    return True, "Usuario creado con éxito"

def crear_estructura_archivos_usuario(username):
    """
    Crea la estructura de archivos para un nuevo usuario
    """
    directorio_usuario = os.path.join(os.path.dirname(__file__), 'datos', username)
    
    # Crear directorio si no existe
    if not os.path.exists(directorio_usuario):
        os.makedirs(directorio_usuario)
    
    # Crear archivos vacíos para ingresos, gastos y objetivos
    archivos = ['incomes.csv', 'expenses.csv', 'goals.csv']
    for archivo in archivos:
        ruta_archivo = os.path.join(directorio_usuario, archivo)
        if not os.path.exists(ruta_archivo):
            # Crear DataFrame vacío con columnas apropiadas
            if archivo == 'incomes.csv':
                columnas = ['date', 'category', 'description', 'amount']
            elif archivo == 'expenses.csv':
                columnas = ['date', 'category', 'description', 'amount']
            else:  # goals.csv
                columnas = ['name', 'target_amount', 'current_amount', 'target_date', 'description']
                
            df = pd.DataFrame(columns=columnas)
            df.to_csv(ruta_archivo, index=False)

def obtener_ruta_archivos_usuario(username):
    """
    Obtiene las rutas de los archivos de datos del usuario
    """
    directorio_usuario = os.path.join(os.path.dirname(__file__), 'datos', username)
    
    return {
        'incomes': os.path.join(directorio_usuario, 'incomes.csv'),
        'expenses': os.path.join(directorio_usuario, 'expenses.csv'),
        'goals': os.path.join(directorio_usuario, 'goals.csv')
    }

def inicializar_sistema():
    """
    Inicializa todo el sistema de usuarios
    """
    # Crear directorio de datos si no existe
    directorio_datos = os.path.join(os.path.dirname(__file__), 'datos')
    if not os.path.exists(directorio_datos):
        os.makedirs(directorio_datos)
    
    # Inicializar archivo de configuración
    inicializar_usuarios() 
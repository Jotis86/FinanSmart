import os
import yaml
import bcrypt
from yaml.loader import SafeLoader
import pandas as pd

def cargar_configuracion():
    """
    Carga la configuración de usuarios desde el archivo YAML
    """
    config_path = os.path.join('config', 'config.yaml')
    
    # Si el archivo no existe, inicializar el sistema
    if not os.path.exists(config_path):
        inicializar_sistema()
    
    # Cargar configuración existente
    with open(config_path, 'r') as file:
        return yaml.load(file, Loader=SafeLoader)

def guardar_configuracion(config):
    """
    Guarda la configuración de usuarios en el archivo YAML
    """
    config_path = os.path.join('config', 'config.yaml')
    os.makedirs('config', exist_ok=True)
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

def crear_usuario(username, name, email, password):
    """
    Crea un nuevo usuario en el sistema
    """
    config = cargar_configuracion()
    
    # Verificar si el usuario ya existe
    if username in config['credentials']['usernames']:
        return False, "El nombre de usuario ya existe"
    
    # Hashear la contraseña
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    # Agregar el nuevo usuario
    config['credentials']['usernames'][username] = {
        'name': name,
        'email': email,
        'password': hashed_password
    }
    
    # Guardar la configuración
    guardar_configuracion(config)
    
    return True, "Usuario creado exitosamente"

def crear_estructura_archivos_usuario(username):
    """
    Crea la estructura de archivos necesaria para un nuevo usuario
    """
    # Crear directorios si no existen
    os.makedirs('data', exist_ok=True)
    os.makedirs('config', exist_ok=True)
    
    # Crear archivos de datos del usuario
    user_data_path = os.path.join('data', username)
    os.makedirs(user_data_path, exist_ok=True)
    
    # Crear archivos CSV vacíos
    pd.DataFrame().to_csv(os.path.join(user_data_path, 'incomes.csv'), index=False)
    pd.DataFrame().to_csv(os.path.join(user_data_path, 'expenses.csv'), index=False)
    pd.DataFrame().to_csv(os.path.join(user_data_path, 'goals.csv'), index=False)

def inicializar_sistema():
    """
    Inicializa el sistema creando los directorios necesarios y el usuario admin
    """
    # Crear directorios necesarios
    os.makedirs('data', exist_ok=True)
    os.makedirs('config', exist_ok=True)
    
    # Crear archivo de configuración con usuario admin si no existe
    config_path = os.path.join('config', 'config.yaml')
    if not os.path.exists(config_path):
        # Crear hash de contraseña para admin
        admin_password = bcrypt.hashpw('admin'.encode(), bcrypt.gensalt()).decode()
        config = {
            'credentials': {
                'usernames': {
                    'admin': {
                        'name': 'Administrador',
                        'email': 'admin@example.com',
                        'password': admin_password
                    }
                }
            }
        }
        with open(config_path, 'w') as file:
            yaml.dump(config, file, default_flow_style=False)
        
        # Crear estructura de archivos para admin
        crear_estructura_archivos_usuario('admin')

def obtener_ruta_archivos_usuario(username):
    """
    Obtiene las rutas de los archivos para un usuario específico
    """
    user_data_path = os.path.join('data', username)
    return {
        'incomes': os.path.join(user_data_path, 'incomes.csv'),
        'expenses': os.path.join(user_data_path, 'expenses.csv'),
        'goals': os.path.join(user_data_path, 'goals.csv')
    } 
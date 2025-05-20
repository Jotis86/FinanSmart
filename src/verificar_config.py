import os
import yaml
import bcrypt
from yaml.loader import SafeLoader

# Ruta del archivo de configuración de usuarios
CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.yaml')

def inicializar_config():
    """
    Inicializa o repara el archivo de configuración para asegurar compatibilidad
    """
    if os.path.exists(CONFIG_PATH):
        try:
            # Intentar cargar la configuración actual
            with open(CONFIG_PATH, 'r') as file:
                config = yaml.load(file, Loader=SafeLoader)
            
            # Verificar si la configuración tiene el formato correcto
            if not config or 'credentials' not in config or 'cookie' not in config:
                raise ValueError("Formato de configuración incorrecto")
            
            print("Archivo de configuración verificado correctamente.")
            return
        except Exception as e:
            print(f"Error al cargar el archivo de configuración: {e}")
            print("Creando nuevo archivo de configuración...")
    
    # Crear configuración predeterminada
    password_hash = bcrypt.hashpw('admin'.encode(), bcrypt.gensalt()).decode()
    
    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'name': 'Administrador',
                    'email': 'admin@example.com',
                    'password': password_hash
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': 'finansmart_auth',
            'name': 'finansmart_cookie'
        }
    }
    
    # Guardar la nueva configuración
    with open(CONFIG_PATH, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    
    print("Nuevo archivo de configuración creado exitosamente.")

if __name__ == "__main__":
    inicializar_config() 
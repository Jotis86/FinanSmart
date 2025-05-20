import os
import sys
import yaml
import bcrypt
from yaml.loader import SafeLoader

def crear_config():
    """
    Crea un archivo de configuración para Streamlit Cloud
    """
    config_path = os.path.join('src', 'config.yaml')
    
    # Crear configuración predeterminada con contraseña hasheada
    password_hash = bcrypt.hashpw('admin'.encode(), bcrypt.gensalt()).decode()
    
    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'name': 'Administrador',
                    'email': 'admin@example.com',
                    'password': password_hash,
                    'failed_login_attempts': 0,
                    'logged_in': False
                }
            }
        },
        'cookie': {
            'expiry_days': 30,
            'key': 'finansmart_auth',
            'name': 'finansmart_cookie'
        }
    }
    
    # Guardar la configuración
    with open(config_path, 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
    
    print(f"Archivo de configuración creado en: {config_path}")
    
    # Crear directorio de datos si no existe
    datos_path = os.path.join('src', 'datos')
    if not os.path.exists(datos_path):
        os.makedirs(datos_path)
        print(f"Directorio de datos creado en: {datos_path}")
    
    # Crear directorio de datos para el usuario admin
    admin_path = os.path.join(datos_path, 'admin')
    if not os.path.exists(admin_path):
        os.makedirs(admin_path)
        print(f"Directorio de datos para admin creado en: {admin_path}")
        
        # Crear archivos vacíos
        for archivo in ['incomes.csv', 'expenses.csv', 'goals.csv']:
            with open(os.path.join(admin_path, archivo), 'w') as f:
                if archivo == 'incomes.csv' or archivo == 'expenses.csv':
                    f.write('date,category,description,amount\n')
                else:  # goals.csv
                    f.write('name,target_amount,current_amount,target_date,description\n')
            print(f"Archivo {archivo} creado para admin")

if __name__ == "__main__":
    crear_config() 
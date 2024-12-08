# Importa AppConfig, que es una clase base para configurar una aplicación de Django
from django.apps import AppConfig


# Definimos una clase de configuración llamada 'MiAppConfig', que hereda de AppConfig
class MiAppConfig(AppConfig):
    # Establece el tipo de campo predeterminado para claves primarias en esta app
    default_auto_field = 'django.db.models.BigAutoField'
    
    # Nombre de la aplicación; debe coincidir con el nombre de la carpeta de la app
    name = 'mi_app'

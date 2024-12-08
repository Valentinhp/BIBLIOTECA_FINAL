"""
ASGI config for mi_proyecto project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

# Importa la biblioteca estándar de Python para manejar configuraciones del sistema operativo
import os

# Importa la función 'get_asgi_application' de Django para configurar el servidor ASGI
from django.core.asgi import get_asgi_application

# Configura la variable de entorno para el módulo de configuración de Django
# Aquí se especifica que las configuraciones están en 'mi_proyecto.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

# Llama a 'get_asgi_application' para crear la aplicación ASGI
# Esto expone la aplicación ASGI que se usará para servir el proyecto en entornos asincrónicos
application = get_asgi_application()

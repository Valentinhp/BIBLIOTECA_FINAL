"""
WSGI config for mi_proyecto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

# Importamos el módulo 'os' para trabajar con configuraciones del sistema operativo
import os

# Importamos la función 'get_wsgi_application' de Django para configurar WSGI
from django.core.wsgi import get_wsgi_application

# Configuramos la variable de entorno 'DJANGO_SETTINGS_MODULE' con el archivo de configuración de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mi_proyecto.settings')

# Llamamos a 'get_wsgi_application' para obtener la aplicación WSGI
# Esto expone la aplicación WSGI que el servidor usará para servir el proyecto
application = get_wsgi_application()

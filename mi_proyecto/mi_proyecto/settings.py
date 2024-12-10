# settings.py

from pathlib import Path  # Importa Path de pathlib para manejar rutas de manera independiente del sistema operativo

# --------------------------------------------------------------------------------
# BASE_DIR: Ruta base del proyecto
# --------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent  # Define la ruta base del proyecto, dos niveles arriba del archivo actual

# --------------------------------------------------------------------------------
# Clave secreta (¡cámbiala en producción!)
# --------------------------------------------------------------------------------

SECRET_KEY = 'tu-clave-secreta-aqui'  # Clave secreta utilizada para proporcionar criptografía y seguridad

# --------------------------------------------------------------------------------
# Modo de depuración (¡desactiva en producción!)
# --------------------------------------------------------------------------------

DEBUG = True  # Activa el modo de depuración. Debe estar en False en producción para seguridad

# --------------------------------------------------------------------------------
# Hosts permitidos
# --------------------------------------------------------------------------------

ALLOWED_HOSTS = []  # Lista de hosts/domains que el sitio puede servir. Vacío significa que no se permiten hosts externos

# --------------------------------------------------------------------------------
# Aplicaciones instaladas
# --------------------------------------------------------------------------------

INSTALLED_APPS = [
    'mi_app',  # Tu aplicación principal
    'django.contrib.admin',  # Interfaz de administración de Django
    'django.contrib.auth',  # Sistema de autenticación de Django
    'django.contrib.contenttypes',  # Framework de tipos de contenido de Django
    'django.contrib.sessions',  # Manejo de sesiones de usuarios
    'django.contrib.messages',  # Sistema de mensajes de Django
    'django.contrib.staticfiles',  # Gestión de archivos estáticos
    'django.contrib.humanize',  # Para mejorar el formato de números/fechas en plantillas
]

# --------------------------------------------------------------------------------
# Middleware
# --------------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Proporciona varias medidas de seguridad
    'django.contrib.sessions.middleware.SessionMiddleware',  # Maneja las sesiones de usuarios
    'django.middleware.locale.LocaleMiddleware',  # Para soporte multiidioma
    'django.middleware.common.CommonMiddleware',  # Proporciona funcionalidades comunes
    'django.middleware.csrf.CsrfViewMiddleware',  # Protección contra ataques CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Maneja la autenticación de usuarios
    'django.contrib.messages.middleware.MessageMiddleware',  # Maneja los mensajes flash
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Protección contra clickjacking
]

# --------------------------------------------------------------------------------
# Configuración de URLs raíz
# --------------------------------------------------------------------------------

ROOT_URLCONF = 'mi_proyecto.urls'  # Especifica el módulo de configuración de URLs raíz del proyecto

# --------------------------------------------------------------------------------
# Configuración de plantillas
# --------------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Utiliza el backend de plantillas de Django
        'DIRS': [BASE_DIR / 'mi_app' / 'templates'],  # Ruta a tus plantillas personalizadas
        'APP_DIRS': True,  # Permite que Django busque plantillas en las carpetas 'templates' de cada app instalada
        'OPTIONS': {
            'context_processors': [  # Procesadores de contexto que inyectan variables en todas las plantillas
                'django.template.context_processors.debug',  # Añade variables de depuración
                'django.template.context_processors.request',  # Añade el objeto 'request' en el contexto
                'django.contrib.auth.context_processors.auth',  # Añade variables de autenticación
                'django.contrib.messages.context_processors.messages',  # Añade mensajes de usuario
            ],
        },
    },
]

# --------------------------------------------------------------------------------
# WSGI application
# --------------------------------------------------------------------------------

WSGI_APPLICATION = 'mi_proyecto.wsgi.application'  # Ruta a la aplicación WSGI utilizada por servidores web para servir el proyecto

# --------------------------------------------------------------------------------
# Configuración de la base de datos (SQLite por defecto)
# --------------------------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Utiliza SQLite como backend de la base de datos
        'NAME': BASE_DIR / 'db.sqlite3',  # Ruta al archivo de la base de datos SQLite
    }
}

# --------------------------------------------------------------------------------
# Validadores de contraseñas
# --------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },  # Valida que la contraseña no sea demasiado similar a otros atributos del usuario
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },  # Valida que la contraseña tenga una longitud mínima
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },  # Valida que la contraseña no sea una contraseña común
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },  # Valida que la contraseña no sea completamente numérica
]

# --------------------------------------------------------------------------------
# Configuración de internacionalización
# --------------------------------------------------------------------------------

LANGUAGE_CODE = 'es'  # Idioma predeterminado del proyecto (Español)

LANGUAGES = [
    ('es', 'Español'),  # Soporte para español
    ('en', 'Inglés'),  # Soporte para inglés
]  # Define los idiomas que la aplicación soporta

LOCALE_PATHS = [BASE_DIR / 'locale']  # Ruta donde se almacenan los archivos de traducción

TIME_ZONE = 'UTC'  # Zona horaria predeterminada del proyecto

USE_I18N = True  # Activa la internacionalización

USE_TZ = True  # Activa el soporte para zonas horarias

# --------------------------------------------------------------------------------
# Configuración de archivos estáticos
# --------------------------------------------------------------------------------

STATIC_URL = '/static/'  # URL a través de la cual se servirán los archivos estáticos

STATICFILES_DIRS = [BASE_DIR / 'mi_app' / 'static']  # Rutas adicionales donde Django buscará archivos estáticos

STATIC_ROOT = BASE_DIR / 'staticfiles'  # Ruta donde se recopilarán los archivos estáticos para producción

# --------------------------------------------------------------------------------
# Configuración de inicio/cierre de sesión
# --------------------------------------------------------------------------------

LOGIN_URL = '/login/'  # URL a la que se redirige a los usuarios no autenticados para que inicien sesión

LOGIN_REDIRECT_URL = 'mi_app:home'  # URL a la que se redirige a los usuarios tras iniciar sesión exitosamente

LOGOUT_REDIRECT_URL = 'mi_app:login'  # URL a la que se redirige a los usuarios tras cerrar sesión

# --------------------------------------------------------------------------------
# Configuración predeterminada para IDs
# --------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'  # Tipo de campo predeterminado para claves primarias auto incrementales

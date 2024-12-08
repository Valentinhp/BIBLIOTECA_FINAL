import os
from pathlib import Path

# BASE_DIR: Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta obtenida desde las variables de entorno (cambiar en producción)
SECRET_KEY = os.getenv('SECRET_KEY', 'clave-predeterminada')

# Modo de depuración dinámico según las variables de entorno
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Hosts permitidos
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')

# Aplicaciones instaladas
INSTALLED_APPS = [
    'mi_app',  # Tu aplicación principal
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',  # Para mejorar el formato de números/fechas
]

# Middleware
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para manejo de estáticos en producción
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Para soporte multiidioma
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URLs raíz
ROOT_URLCONF = 'mi_proyecto.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'mi_app' / 'templates'],  # Ruta a tus plantillas
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Necesario para auth
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI application
WSGI_APPLICATION = 'mi_proyecto.wsgi.application'

# Configuración de la base de datos
# Usa PostgreSQL en Render o SQLite por defecto
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

# Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Configuración de internacionalización
LANGUAGE_CODE = 'es'  # Idioma predeterminado (Español)
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'Inglés'),
]  # Soporte multiidioma
LOCALE_PATHS = [BASE_DIR / 'locale']

TIME_ZONE = 'UTC'  # Zona horaria
USE_I18N = True
USE_TZ = True

# Configuración de archivos estáticos
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'mi_app' / 'static']  # Ruta a archivos estáticos
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Almacenamiento de archivos estáticos en producción
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Configuración de inicio/cierre de sesión
LOGIN_URL = '/login/'  # Redirección si no está autenticado
LOGIN_REDIRECT_URL = 'mi_app:home'  # Redirección tras iniciar sesión
LOGOUT_REDIRECT_URL = 'mi_app:login'  # Redirección tras cerrar sesión

# Configuración predeterminada para IDs
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de logging en producción
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

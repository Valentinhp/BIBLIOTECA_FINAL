# mi_proyecto/urls.py

from django.contrib import admin  # Importa el módulo de administración de Django
from django.urls import path, include  # Importa las funciones para definir rutas
from django.views.generic import RedirectView  # Importa la vista genérica para redirecciones

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta al panel de administración de Django
    path('', include('mi_app.urls')),  # Incluye las URLs definidas en 'mi_app/urls.py'

    # --------------------------------------------------------------------------------
    # Redirecciones para autenticación
    # --------------------------------------------------------------------------------

    # Redirige las solicitudes a '/accounts/login/' a '/login/' sin ser una redirección permanente
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False)),

    # (Opcional) Redirige las solicitudes a '/accounts/logout/' a '/logout/' sin ser una redirección permanente
    path('accounts/logout/', RedirectView.as_view(url='/logout/', permanent=False)),
]

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),  # Ruta al panel de administración
    path('', include('mi_app.urls')),  # Incluir las URLs de mi_app

    # Redirigir /accounts/login/ a /login/
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False)),
    
    # (Opcional) Redirigir /accounts/logout/ a /logout/
    path('accounts/logout/', RedirectView.as_view(url='/logout/', permanent=False)),
]

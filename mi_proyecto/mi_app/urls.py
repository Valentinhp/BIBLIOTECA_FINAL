from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'mi_app'

urlpatterns = [
    # Páginas principales
    path('', views.home, name='home'),  # Página principal (Home)
    path('acerca/', views.acerca, name='acerca'),  # Página "Acerca de"
    path('index/', views.index, name='index'),  # Página protegida (Index)

    # Autenticación
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),

    # Rutas para Autores
    path('autores/', views.obtener_autores, name='obtener_autores'),
    path('autores/agregar/', views.agregar_autor, name='agregar_autor'),
    path('autores/editar/<int:autor_id>/', views.editar_autor, name='editar_autor'),
    path('autores/eliminar/<int:autor_id>/', views.eliminar_autor, name='eliminar_autor'),
    path('autores/buscar/', views.buscar_autores, name='buscar_autores'),

    # Rutas para Libros
    path('libros/', views.obtener_libros, name='obtener_libros'),
    path('libros/<int:libro_id>/', views.obtener_libro, name='obtener_libro'),
    path('libros/agregar/', views.agregar_libro, name='agregar_libro'),
    path('libros/editar/<int:libro_id>/', views.editar_libro, name='editar_libro'),
    path('libros/eliminar/<int:libro_id>/', views.eliminar_libro, name='eliminar_libro'),

    # Rutas para Comentarios
    path('libros/<int:libro_id>/comentarios/', views.obtener_comentarios, name='obtener_comentarios'),
    path('libros/<int:libro_id>/comentarios/agregar/', views.agregar_comentario, name='agregar_comentario'),
    path('comentarios/editar/<int:comentario_id>/', views.editar_comentario, name='editar_comentario'),
    path('comentarios/eliminar/<int:comentario_id>/', views.eliminar_comentario, name='eliminar_comentario'),
    path('comentarios/todos/', views.obtener_todos_comentarios, name='obtener_todos_comentarios'),

    # Opcional: redirecciones para cuentas
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login_accounts'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout_accounts'),
    path('acerca/', views.acerca, name='acerca'),
]

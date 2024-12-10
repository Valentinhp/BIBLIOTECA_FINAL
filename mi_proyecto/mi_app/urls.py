# mi_app/urls.py

# Importa la función 'path' para definir rutas URL en Django
from django.urls import path

# Importa las vistas de autenticación de Django y las renombra como 'auth_views' para evitar conflictos
from django.contrib.auth import views as auth_views

# Importa las vistas personalizadas definidas en 'views.py' del mismo directorio
from . import views

# Define un espacio de nombres para las rutas de esta aplicación
# Esto es útil para evitar conflictos de nombres cuando múltiples aplicaciones tienen rutas con el mismo nombre
app_name = 'mi_app'

# Lista de patrones de URL que mapean rutas específicas a funciones o clases de vistas
urlpatterns = [
    # -------------------------------------
    # Páginas Principales de la Aplicación
    # -------------------------------------
    
    # Ruta para la página principal (Home)
    # URL: dominio.com/
    path('', views.home, name='home'),  # Asocia la ruta raíz con la vista 'home' y le asigna el nombre 'home'
    
    # Ruta para la página "Acerca de"
    # URL: dominio.com/acerca/
    path('acerca/', views.acerca, name='acerca'),  # Asocia la ruta 'acerca/' con la vista 'acerca' y le asigna el nombre 'acerca'
    
    # Ruta para la página protegida (Index)
    # URL: dominio.com/index/
    path('index/', views.index, name='index'),  # Asocia la ruta 'index/' con la vista 'index' y le asigna el nombre 'index'
    
    # -----------------
    # Rutas de Autenticación
    # -----------------
    
    # Ruta para la página de inicio de sesión (Login)
    # Utiliza la vista genérica de inicio de sesión de Django con una plantilla personalizada
    # URL: dominio.com/login/
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),  # Especifica la plantilla HTML para el formulario de login
        name='login'  # Asigna el nombre 'login' a esta ruta para facilitar su referencia en plantillas y vistas
    ),
    
    # Ruta para la página de registro de nuevos usuarios (Signup)
    # URL: dominio.com/signup/
    path(
        'signup/',
        views.signup,  # Asocia la ruta 'signup/' con la vista personalizada 'signup' definida en 'views.py'
        name='signup'  # Asigna el nombre 'signup' a esta ruta
    ),
    
    # Ruta para cerrar sesión (Logout)
    # URL: dominio.com/logout/
    path(
        'logout/',
        views.user_logout,  # Asocia la ruta 'logout/' con la vista personalizada 'user_logout' definida en 'views.py'
        name='logout'  # Asigna el nombre 'logout' a esta ruta
    ),
    
    # -----------------
    # Rutas para Autores
    # -----------------
    
    # Ruta para obtener la lista de autores
    # URL: dominio.com/autores/
    path(
        'autores/',
        views.obtener_autores,  # Asocia la ruta 'autores/' con la vista 'obtener_autores' para manejar solicitudes de obtención de autores
        name='obtener_autores'  # Asigna el nombre 'obtener_autores' a esta ruta
    ),
    
    # Ruta para agregar un nuevo autor
    # URL: dominio.com/autores/agregar/
    path(
        'autores/agregar/',
        views.agregar_autor,  # Asocia la ruta 'autores/agregar/' con la vista 'agregar_autor' para manejar la creación de nuevos autores
        name='agregar_autor'  # Asigna el nombre 'agregar_autor' a esta ruta
    ),
    
    # Ruta para editar un autor existente
    # URL: dominio.com/autores/editar/<autor_id>/
    # <autor_id> es un parámetro que captura el ID del autor a editar y lo pasa a la vista
    path(
        'autores/editar/<int:autor_id>/',  # Define una ruta que incluye un parámetro entero 'autor_id'
        views.editar_autor,  # Asocia la ruta con la vista 'editar_autor' para manejar la edición de un autor específico
        name='editar_autor'  # Asigna el nombre 'editar_autor' a esta ruta
    ),
    
    # Ruta para eliminar un autor existente
    # URL: dominio.com/autores/eliminar/<autor_id>/
    # <autor_id> es un parámetro que captura el ID del autor a eliminar y lo pasa a la vista
    path(
        'autores/eliminar/<int:autor_id>/',  # Define una ruta que incluye un parámetro entero 'autor_id'
        views.eliminar_autor,  # Asocia la ruta con la vista 'eliminar_autor' para manejar la eliminación de un autor específico
        name='eliminar_autor'  # Asigna el nombre 'eliminar_autor' a esta ruta
    ),
    
    # Ruta para buscar autores (usada principalmente por AJAX en Select2)
    # URL: dominio.com/autores/buscar/
    path(
        'autores/buscar/',
        views.buscar_autores,  # Asocia la ruta 'autores/buscar/' con la vista 'buscar_autores' para manejar búsquedas de autores
        name='buscar_autores'  # Asigna el nombre 'buscar_autores' a esta ruta
    ),
    
    # -----------------
    # Rutas para Libros
    # -----------------
    
    # Ruta para obtener la lista de libros
    # URL: dominio.com/libros/
    path(
        'libros/',
        views.obtener_libros,  # Asocia la ruta 'libros/' con la vista 'obtener_libros' para manejar solicitudes de obtención de libros
        name='obtener_libros'  # Asigna el nombre 'obtener_libros' a esta ruta
    ),
    
    # Ruta para obtener detalles de un libro específico
    # URL: dominio.com/libros/<libro_id>/
    # <libro_id> es un parámetro que captura el ID del libro y lo pasa a la vista
    path(
        'libros/<int:libro_id>/',  # Define una ruta que incluye un parámetro entero 'libro_id'
        views.obtener_libro,  # Asocia la ruta con la vista 'obtener_libro' para manejar la obtención de un libro específico
        name='obtener_libro'  # Asigna el nombre 'obtener_libro' a esta ruta
    ),
    
    # Ruta para agregar un nuevo libro
    # URL: dominio.com/libros/agregar/
    path(
        'libros/agregar/',
        views.agregar_libro,  # Asocia la ruta 'libros/agregar/' con la vista 'agregar_libro' para manejar la creación de nuevos libros
        name='agregar_libro'  # Asigna el nombre 'agregar_libro' a esta ruta
    ),
    
    # Ruta para editar un libro existente
    # URL: dominio.com/libros/editar/<libro_id>/
    # <libro_id> es un parámetro que captura el ID del libro a editar y lo pasa a la vista
    path(
        'libros/editar/<int:libro_id>/',  # Define una ruta que incluye un parámetro entero 'libro_id'
        views.editar_libro,  # Asocia la ruta con la vista 'editar_libro' para manejar la edición de un libro específico
        name='editar_libro'  # Asigna el nombre 'editar_libro' a esta ruta
    ),
    
    # Ruta para eliminar un libro existente
    # URL: dominio.com/libros/eliminar/<libro_id>/
    # <libro_id> es un parámetro que captura el ID del libro a eliminar y lo pasa a la vista
    path(
        'libros/eliminar/<int:libro_id>/',  # Define una ruta que incluye un parámetro entero 'libro_id'
        views.eliminar_libro,  # Asocia la ruta con la vista 'eliminar_libro' para manejar la eliminación de un libro específico
        name='eliminar_libro'  # Asigna el nombre 'eliminar_libro' a esta ruta
    ),
    
    # ---------------------
    # Rutas para Comentarios
    # ---------------------
    
    # Ruta para obtener los comentarios de un libro específico
    # URL: dominio.com/libros/<libro_id>/comentarios/
    # <libro_id> es un parámetro que captura el ID del libro cuyos comentarios se desean obtener
    path(
        'libros/<int:libro_id>/comentarios/',
        views.obtener_comentarios,  # Asocia la ruta con la vista 'obtener_comentarios' para manejar la obtención de comentarios de un libro específico
        name='obtener_comentarios'  # Asigna el nombre 'obtener_comentarios' a esta ruta
    ),
    
    # Ruta para agregar un nuevo comentario a un libro específico
    # URL: dominio.com/libros/<libro_id>/comentarios/agregar/
    # <libro_id> es un parámetro que captura el ID del libro al que se agregará el comentario
    path(
        'libros/<int:libro_id>/comentarios/agregar/',
        views.agregar_comentario,  # Asocia la ruta con la vista 'agregar_comentario' para manejar la creación de nuevos comentarios en un libro específico
        name='agregar_comentario'  # Asigna el nombre 'agregar_comentario' a esta ruta
    ),
    
    # Ruta para editar un comentario existente
    # URL: dominio.com/comentarios/editar/<comentario_id>/
    # <comentario_id> es un parámetro que captura el ID del comentario a editar y lo pasa a la vista
    path(
        'comentarios/editar/<int:comentario_id>/',  # Define una ruta que incluye un parámetro entero 'comentario_id'
        views.editar_comentario,  # Asocia la ruta con la vista 'editar_comentario' para manejar la edición de un comentario específico
        name='editar_comentario'  # Asigna el nombre 'editar_comentario' a esta ruta
    ),
    
    # Ruta para eliminar un comentario existente
    # URL: dominio.com/comentarios/eliminar/<comentario_id>/
    # <comentario_id> es un parámetro que captura el ID del comentario a eliminar y lo pasa a la vista
    path(
        'comentarios/eliminar/<int:comentario_id>/',  # Define una ruta que incluye un parámetro entero 'comentario_id'
        views.eliminar_comentario,  # Asocia la ruta con la vista 'eliminar_comentario' para manejar la eliminación de un comentario específico
        name='eliminar_comentario'  # Asigna el nombre 'eliminar_comentario' a esta ruta
    ),
    
    # Ruta para obtener todos los comentarios de todos los libros
    # URL: dominio.com/comentarios/todos/
    path(
        'comentarios/todos/',
        views.obtener_todos_comentarios,  # Asocia la ruta 'comentarios/todos/' con la vista 'obtener_todos_comentarios' para manejar la obtención de todos los comentarios
        name='obtener_todos_comentarios'  # Asigna el nombre 'obtener_todos_comentarios' a esta ruta
    ),
    
    # ----------------------------
    # Rutas Opcionales para Cuentas
    # ----------------------------
    
    # Ruta adicional para la página de inicio de sesión (Login) en el espacio de nombres 'accounts'
    # URL: dominio.com/accounts/login/
    path(
        'accounts/login/',
        auth_views.LoginView.as_view(template_name='registration/login.html'),  # Utiliza la vista genérica de inicio de sesión con una plantilla personalizada
        name='login_accounts'  # Asigna el nombre 'login_accounts' a esta ruta para diferenciarla de otras rutas de login
    ),
    
    # Ruta adicional para cerrar sesión (Logout) en el espacio de nombres 'accounts'
    # URL: dominio.com/accounts/logout/
    path(
        'accounts/logout/',
        auth_views.LogoutView.as_view(),  # Utiliza la vista genérica de cierre de sesión de Django
        name='logout_accounts'  # Asigna el nombre 'logout_accounts' a esta ruta para diferenciarla de otras rutas de logout
    ),
    
    # Ruta duplicada para la página "Acerca de"
    # URL: dominio.com/acerca/
    # Nota: Esta ruta ya está definida anteriormente. Es recomendable eliminarla para evitar conflictos.
    path(
        'acerca/',
        views.acerca,  # Asocia la ruta 'acerca/' con la vista 'acerca' nuevamente
        name='acerca'  # Asigna el nombre 'acerca' a esta ruta
    ),
]

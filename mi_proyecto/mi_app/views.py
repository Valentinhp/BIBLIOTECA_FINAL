# mi_app/views.py

# Importaciones necesarias de Django para manejar las vistas y funcionalidades relacionadas
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Autor, Libro, Comentario
import json
from django.db.models import Q

# --------------------------------------------------------------------------------
# Vistas Generales (Páginas Principales y Autenticación)
# --------------------------------------------------------------------------------

def home(request):
    """
    Vista para la página principal (Home).
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
    
    Returns:
        HttpResponse: Renderiza la plantilla 'home.html'.
    """
    return render(request, 'mi_app/home.html')  # Renderiza la plantilla 'home.html' ubicada en 'mi_app/templates/mi_app/'


def acerca(request):
    """
    Vista para la página "Acerca de".
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
    
    Returns:
        HttpResponse: Renderiza la plantilla 'acerca_de.html'.
    """
    return render(request, 'mi_app/acerca_de.html')  # Renderiza la plantilla 'acerca_de.html'


@login_required
def index(request):
    """
    Vista para la página protegida (Index).
    Solo accesible para usuarios autenticados.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
    
    Returns:
        HttpResponse: Renderiza la plantilla 'index.html'.
    """
    return render(request, 'mi_app/index.html')  # Renderiza la plantilla 'index.html'


def signup(request):
    """
    Vista para el registro de nuevos usuarios.
    
    Maneja tanto solicitudes GET como POST.
    - GET: Muestra el formulario de registro.
    - POST: Procesa los datos del formulario, crea un nuevo usuario y lo autentica.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
    
    Returns:
        HttpResponse: Renderiza la plantilla 'signup.html' con el formulario de registro o redirige al 'home' tras el registro exitoso.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # Instancia el formulario de creación de usuario con los datos enviados
        if form.is_valid():
            user = form.save()  # Guarda el nuevo usuario en la base de datos
            login(request, user)  # Autentica al usuario recién creado
            messages.success(request, "¡Registro exitoso! Bienvenido.")  # Muestra un mensaje de éxito al usuario
            return redirect('mi_app:home')  # Redirige al usuario a la página principal
    else:
        form = UserCreationForm()  # Instancia un formulario vacío para solicitudes GET
    return render(request, 'registration/signup.html', {'form': form})  # Renderiza el formulario de registro


def user_logout(request):
    """
    Vista para cerrar la sesión del usuario.
    
    Cierra la sesión actual, muestra un mensaje informativo y redirige al usuario a la página de inicio de sesión.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
    
    Returns:
        HttpResponse: Redirige al usuario a la página de inicio de sesión con un mensaje de confirmación.
    """
    logout(request)  # Cierra la sesión del usuario actual
    messages.info(request, "Has cerrado sesión exitosamente.")  # Muestra un mensaje informativo
    return redirect('mi_app:login')  # Redirige al usuario a la página de inicio de sesión

# --------------------------------------------------------------------------------
# Vistas para Autores
# --------------------------------------------------------------------------------

@login_required
def obtener_autores(request):
    """
    Vista para obtener la lista de todos los autores.
    
    Retorna una respuesta JSON con los IDs y nombres de los autores.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
    
    Returns:
        JsonResponse: Lista de autores en formato JSON.
    """
    autores = Autor.objects.all().values('id', 'nombre')  # Obtiene todos los autores con sus IDs y nombres
    return JsonResponse(list(autores), safe=False)  # Retorna la lista de autores como JSON


@login_required
@require_POST
def agregar_autor(request):
    """
    Vista para agregar un nuevo autor.
    
    Solo acepta solicitudes POST realizadas mediante AJAX.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
    
    Returns:
        JsonResponse: Respuesta JSON indicando el éxito o error de la operación.
    """
    # Verifica que la solicitud se realice mediante AJAX
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)  # Método no permitido
    
    try:
        data = json.loads(request.body)  # Carga los datos JSON enviados en el cuerpo de la solicitud
        nombre = data.get('nombre', '').strip()  # Obtiene el nombre del autor y elimina espacios en blanco
        
        if not nombre:
            return JsonResponse({'error': 'El nombre del autor es requerido.'}, status=400)  # Error si el nombre está vacío
        
        # Crea un nuevo autor o obtiene uno existente con el mismo nombre
        nuevo_autor, created = Autor.objects.get_or_create(nombre=nombre)
        
        if created:
            # Retorna los detalles del nuevo autor si se creó exitosamente
            return JsonResponse({'autor_id': nuevo_autor.id, 'nombre': nuevo_autor.nombre}, status=201)
        else:
            # Retorna un error si el autor ya existe
            return JsonResponse({'error': 'El autor ya existe.'}, status=400)
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)  # Error si los datos JSON son inválidos


@login_required
@require_POST
def editar_autor(request, autor_id):
    """
    Vista para editar un autor existente.
    
    Solo accesible para usuarios administradores (staff).
    Solo acepta solicitudes POST realizadas mediante AJAX.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        autor_id (int): ID del autor a editar.
    
    Returns:
        JsonResponse: Respuesta JSON indicando el éxito o error de la operación.
    """
    # Verifica si el usuario tiene permisos de administrador
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para editar autores.'}, status=403)  # Permiso denegado
    
    # Verifica que la solicitud se realice mediante AJAX
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)  # Método no permitido
    
    try:
        data = json.loads(request.body)  # Carga los datos JSON enviados en el cuerpo de la solicitud
        nuevo_nombre = data.get('nombre', '').strip()  # Obtiene el nuevo nombre del autor y elimina espacios en blanco
        
        if not nuevo_nombre:
            return JsonResponse({'error': 'El nombre del autor no puede estar vacío'}, status=400)  # Error si el nombre está vacío
        
        autor = get_object_or_404(Autor, id=autor_id)  # Obtiene el autor o retorna 404 si no existe
        autor.nombre = nuevo_nombre  # Actualiza el nombre del autor
        autor.save()  # Guarda los cambios en la base de datos
        
        return JsonResponse({'mensaje': 'Autor actualizado correctamente'})  # Retorna un mensaje de éxito
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)  # Error si los datos JSON son inválidos


@login_required
@require_POST
def eliminar_autor(request, autor_id):
    """
    Vista para eliminar un autor existente.
    
    Solo accesible para usuarios administradores (staff).
    Solo acepta solicitudes POST realizadas mediante AJAX.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        autor_id (int): ID del autor a eliminar.
    
    Returns:
        JsonResponse: Respuesta JSON indicando el éxito o error de la operación.
    """
    # Verifica si el usuario tiene permisos de administrador
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para eliminar autores.'}, status=403)  # Permiso denegado
    
    # Verifica que la solicitud se realice mediante AJAX
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)  # Método no permitido
    
    try:
        autor = get_object_or_404(Autor, id=autor_id)  # Obtiene el autor o retorna 404 si no existe
        autor.delete()  # Elimina el autor de la base de datos
        return JsonResponse({'mensaje': 'Autor eliminado correctamente'})  # Retorna un mensaje de éxito
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)  # Retorna cualquier otro error ocurrido durante la eliminación


@login_required
def buscar_autores(request):
    """
    Vista para buscar autores basados en una consulta.
    
    Utilizada principalmente por AJAX en campos de selección como Select2.
    Solo acepta solicitudes GET realizadas mediante AJAX.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
    
    Returns:
        JsonResponse: Lista de autores que coinciden con la consulta en formato JSON.
    """
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '')  # Obtiene el parámetro de búsqueda 'q' de la URL
        # Filtra los autores cuyos nombres contienen la consulta (insensible a mayúsculas)
        autores = Autor.objects.filter(Q(nombre__icontains=query))[:10]  # Limita los resultados a los primeros 10 autores encontrados
        # Prepara los resultados para Select2 en formato {'id': ..., 'text': ...}
        resultados = [{'id': autor.id, 'text': autor.nombre} for autor in autores]
        return JsonResponse({'results': resultados})  # Retorna los resultados como JSON
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)  # Método no permitido si no se cumplen las condiciones

# --------------------------------------------------------------------------------
# Vistas para Libros
# --------------------------------------------------------------------------------

@login_required
def obtener_libros(request):
    """
    Vista para obtener la lista de todos los libros.
    
    Retorna una respuesta JSON con detalles de cada libro, incluyendo sus autores.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
    
    Returns:
        JsonResponse: Lista de libros en formato JSON.
    """
    libros = Libro.objects.prefetch_related('autores').all()  # Obtiene todos los libros y prefetches sus autores para optimizar consultas
    data = [
        {
            'id': libro.id,
            'titulo': libro.titulo,
            'autores_nombres': ", ".join([autor.nombre for autor in libro.autores.all()]),  # Combina los nombres de los autores en una sola cadena separada por comas
            'anio_publicacion': libro.anio_publicacion,
            'idioma': libro.idioma,
        }
        for libro in libros
    ]
    return JsonResponse({'data': data})  # Retorna la lista de libros como JSON


@login_required
def obtener_libro(request, libro_id):
    """
    Vista para obtener los detalles de un libro específico.
    
    Retorna una respuesta JSON con los detalles del libro, incluyendo sus autores.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        libro_id (int): ID del libro a obtener.
    
    Returns:
        JsonResponse: Detalles del libro en formato JSON.
    """
    libro = get_object_or_404(Libro, id=libro_id)  # Obtiene el libro o retorna 404 si no existe
    autores = libro.autores.all()  # Obtiene todos los autores relacionados con el libro
    data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'anio_publicacion': libro.anio_publicacion,
        'idioma': libro.idioma,
        'autores': [{'id': autor.id, 'nombre': autor.nombre} for autor in autores],  # Lista de autores con sus IDs y nombres
    }
    return JsonResponse(data)  # Retorna los detalles del libro como JSON


@login_required
@require_POST
def agregar_libro(request):
    """
    Vista para agregar un nuevo libro.
    
    Solo acepta solicitudes POST realizadas mediante AJAX.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
    
    Returns:
        JsonResponse: Respuesta JSON indicando el éxito o error de la operación.
    """
    # Verifica que la solicitud se realice mediante AJAX
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)  # Método no permitido
    
    try:
        data = json.loads(request.body)  # Carga los datos JSON enviados en el cuerpo de la solicitud
        titulo = data.get('titulo', '').strip()  # Obtiene el título del libro y elimina espacios en blanco
        anio_publicacion = data.get('anio_publicacion')  # Obtiene el año de publicación
        idioma = data.get('idioma', '').strip()  # Obtiene el idioma y elimina espacios en blanco
        autor_ids = data.get('autores', [])  # Obtiene la lista de IDs de autores seleccionados
        
        # Verifica que todos los campos sean proporcionados y válidos
        if not (titulo and anio_publicacion and idioma and autor_ids):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)  # Error si faltan campos
        
        # Filtra los autores que coinciden con los IDs proporcionados
        autores = Autor.objects.filter(id__in=autor_ids)
        if not autores.exists():
            return JsonResponse({'error': 'Selecciona al menos un autor válido'}, status=400)  # Error si no hay autores válidos seleccionados
        
        # Crea el nuevo libro con los datos proporcionados
        libro = Libro.objects.create(
            titulo=titulo,
            anio_publicacion=anio_publicacion,
            idioma=idioma
        )
        libro.autores.set(autores)  # Asocia los autores al libro
        
        return JsonResponse({'mensaje': 'Libro agregado correctamente'}, status=201)  # Retorna un mensaje de éxito
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)  # Error si los datos JSON son inválidos


@login_required
@require_POST
def editar_libro(request, libro_id):
    """
    Vista para editar un libro existente.
    
    Solo accesible para usuarios administradores (staff).
    Solo acepta solicitudes POST realizadas mediante AJAX.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        libro_id (int): ID del libro a editar.
    
    Returns:
        JsonResponse: Respuesta JSON indicando el éxito o error de la operación.
    """
    # Verifica si el usuario tiene permisos de administrador
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para editar libros.'}, status=403)  # Permiso denegado
    
    # Verifica que la solicitud se realice mediante AJAX
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)  # Método no permitido
    
    try:
        data = json.loads(request.body)  # Carga los datos JSON enviados en el cuerpo de la solicitud
        titulo = data.get('titulo', '').strip()  # Obtiene el nuevo título del libro y elimina espacios en blanco
        anio_publicacion = data.get('anio_publicacion')  # Obtiene el nuevo año de publicación
        idioma = data.get('idioma', '').strip()  # Obtiene el nuevo idioma y elimina espacios en blanco
        autor_ids = data.get('autores', [])  # Obtiene la nueva lista de IDs de autores seleccionados
        
        # Verifica que todos los campos sean proporcionados y válidos
        if not (titulo and anio_publicacion and idioma and autor_ids):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)  # Error si faltan campos
        
        # Filtra los autores que coinciden con los nuevos IDs proporcionados
        autores = Autor.objects.filter(id__in=autor_ids)
        if not autores.exists():
            return JsonResponse({'error': 'Selecciona al menos un autor válido'}, status=400)  # Error si no hay autores válidos seleccionados
        
        libro = get_object_or_404(Libro, id=libro_id)  # Obtiene el libro o retorna 404 si no existe
        libro.titulo = titulo  # Actualiza el título del libro
        libro.anio_publicacion = anio_publicacion  # Actualiza el año de publicación
        libro.idioma = idioma  # Actualiza el idioma
        libro.autores.set(autores)  # Actualiza la lista de autores asociados al libro
        libro.save()  # Guarda los cambios en la base de datos
        
        return JsonResponse({'mensaje': 'Libro actualizado correctamente'})  # Retorna un mensaje de éxito
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)  # Error si los datos JSON son inválidos


@login_required
@require_POST
def eliminar_libro(request, libro_id):
    """
    Vista para eliminar un libro existente.
    
    Solo accesible para usuarios administradores (staff).
    Solo acepta solicitudes POST realizadas mediante AJAX.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        libro_id (int): ID del libro a eliminar.
    
    Returns:
        JsonResponse: Respuesta JSON indicando el éxito o error de la operación.
    """
    # Verifica si el usuario tiene permisos de administrador
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para eliminar libros.'}, status=403)  # Permiso denegado
    
    # Verifica que la solicitud se realice mediante AJAX
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)  # Método no permitido
    
    try:
        libro = get_object_or_404(Libro, id=libro_id)  # Obtiene el libro o retorna 404 si no existe
        libro.delete()  # Elimina el libro de la base de datos
        return JsonResponse({'mensaje': 'Libro eliminado correctamente'})  # Retorna un mensaje de éxito
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)  # Retorna cualquier otro error ocurrido durante la eliminación

# --------------------------------------------------------------------------------
# Vistas para Comentarios
# --------------------------------------------------------------------------------

@login_required
def obtener_comentarios(request, libro_id):
    """
    Vista para obtener los comentarios de un libro específico.
    
    Retorna una respuesta JSON con los comentarios del libro.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        libro_id (int): ID del libro cuyos comentarios se desean obtener.
    
    Returns:
        JsonResponse: Lista de comentarios en formato JSON.
    """
    libro = get_object_or_404(Libro, id=libro_id)  # Obtiene el libro o retorna 404 si no existe
    comentarios = libro.comentarios.all().values('id', 'usuario__username', 'texto', 'fecha')  # Obtiene los comentarios relacionados con el libro
    
    return JsonResponse(list(comentarios), safe=False)  # Retorna la lista de comentarios como JSON


@login_required
@require_POST
def agregar_comentario(request, libro_id):
    """
    Vista para agregar un nuevo comentario a un libro específico.
    
    Solo acepta solicitudes POST realizadas mediante AJAX.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        libro_id (int): ID del libro al que se agregará el comentario.
    
    Returns:
        JsonResponse: Respuesta JSON indicando el éxito o error de la operación, y detalles del comentario creado.
    """
    # Verifica que la solicitud se realice mediante AJAX
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)  # Método no permitido
    
    try:
        data = json.loads(request.body)  # Carga los datos JSON enviados en el cuerpo de la solicitud
        texto = data.get("texto", "").strip()  # Obtiene el texto del comentario y elimina espacios en blanco
        
        if texto:
            libro = get_object_or_404(Libro, id=libro_id)  # Obtiene el libro o retorna 404 si no existe
            comentario = Comentario.objects.create(
                libro=libro,  # Asocia el comentario al libro
                usuario=request.user,  # Asocia el comentario al usuario actual
                texto=texto  # Texto del comentario
            )
            # Prepara los detalles del comentario para la respuesta JSON
            return JsonResponse({
                'mensaje': 'Comentario agregado correctamente',
                'comentario': {
                    'id': comentario.id,
                    'usuario__username': comentario.usuario.username,
                    'texto': comentario.texto,
                    'fecha': comentario.fecha.strftime('%Y-%m-%d %H:%M'),  # Formatea la fecha
                }
            }, status=201)  # Retorna un mensaje de éxito y detalles del comentario creado
        
        return JsonResponse({'error': 'El comentario no puede estar vacío.'}, status=400)  # Error si el texto está vacío
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)  # Error si los datos JSON son inválidos


@login_required
@require_POST
def editar_comentario(request, comentario_id):
    """
    Vista para editar un comentario existente.
    
    Solo acepta solicitudes POST realizadas mediante AJAX.
    Solo puede ser editado por el usuario que lo creó o por un administrador.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        comentario_id (int): ID del comentario a editar.
    
    Returns:
        JsonResponse: Respuesta JSON indicando el éxito o error de la operación.
    """
    # Verifica que la solicitud se realice mediante AJAX
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)  # Método no permitido
    
    comentario = get_object_or_404(Comentario, id=comentario_id)  # Obtiene el comentario o retorna 404 si no existe
    
    # Verifica si el usuario actual es el autor del comentario o un administrador
    if comentario.usuario != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para editar este comentario.'}, status=403)  # Permiso denegado
    
    try:
        data = json.loads(request.body)  # Carga los datos JSON enviados en el cuerpo de la solicitud
        nuevo_texto = data.get('texto', '').strip()  # Obtiene el nuevo texto del comentario y elimina espacios en blanco
        
        if nuevo_texto:
            comentario.texto = nuevo_texto  # Actualiza el texto del comentario
            comentario.save()  # Guarda los cambios en la base de datos
            return JsonResponse({'mensaje': 'Comentario actualizado correctamente'})  # Retorna un mensaje de éxito
        
        return JsonResponse({'error': 'El texto del comentario no puede estar vacío'}, status=400)  # Error si el texto está vacío
    
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)  # Error si los datos JSON son inválidos


@login_required
@require_POST
def eliminar_comentario(request, comentario_id):
    """
    Vista para eliminar un comentario existente.
    
    Solo acepta solicitudes POST realizadas mediante AJAX.
    Solo puede ser eliminado por el usuario que lo creó o por un administrador.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
        comentario_id (int): ID del comentario a eliminar.
    
    Returns:
        JsonResponse: Respuesta JSON indicando el éxito o error de la operación.
    """
    # Verifica que la solicitud se realice mediante AJAX
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)  # Método no permitido
    
    comentario = get_object_or_404(Comentario, id=comentario_id)  # Obtiene el comentario o retorna 404 si no existe
    
    # Verifica si el usuario actual es el autor del comentario o un administrador
    if comentario.usuario != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para eliminar este comentario.'}, status=403)  # Permiso denegado
    
    try:
        comentario.delete()  # Elimina el comentario de la base de datos
        return JsonResponse({'mensaje': 'Comentario eliminado correctamente'})  # Retorna un mensaje de éxito
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)  # Retorna cualquier otro error ocurrido durante la eliminación


@login_required
def obtener_todos_comentarios(request):
    """
    Vista para obtener todos los comentarios de todos los libros.
    
    Retorna una respuesta JSON con detalles de cada comentario.
    
    Args:
        request (HttpRequest): Objeto de solicitud HTTP.
    
    Returns:
        JsonResponse: Lista de comentarios en formato JSON.
    """
    # Utiliza select_related para optimizar las consultas relacionadas con 'libro' y 'usuario'
    comentarios = Comentario.objects.select_related('libro', 'usuario').all().values(
        'id',
        'libro__titulo',
        'usuario__username',
        'texto',
        'fecha'
    )
    return JsonResponse(list(comentarios), safe=False)  # Retorna la lista de comentarios como JSON


# --------------------------------------------------------------------------------
# Nota Importante:
# --------------------------------------------------------------------------------

# Al final del código proporcionado, hay una definición duplicada de la vista 'acerca'.
# Esto puede causar conflictos y comportamientos inesperados.
# Asegúrate de eliminar una de las definiciones para evitar problemas.

def acerca(request):
    return render(request, 'mi_app/acerca_de.html')  # Esta definición está duplicada y debe ser removida si ya existe anteriormente

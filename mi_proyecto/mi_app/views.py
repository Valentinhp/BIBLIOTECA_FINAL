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

# Página principal (Home)
def home(request):
    return render(request, 'mi_app/home.html')

# Página "Acerca de"
def acerca(request):
    return render(request, 'mi_app/acerca_de.html')

# Página protegida (Index)
@login_required
def index(request):
    return render(request, 'mi_app/index.html')

# Registro de usuarios
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "¡Registro exitoso! Bienvenido.")
            return redirect('mi_app:home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Cerrar sesión
def user_logout(request):
    logout(request)
    messages.info(request, "Has cerrado sesión exitosamente.")
    return redirect('mi_app:login')

# Vistas para Autores
@login_required
def obtener_autores(request):
    autores = Autor.objects.all().values('id', 'nombre')
    return JsonResponse(list(autores), safe=False)

@login_required
@require_POST
def agregar_autor(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        if not nombre:
            return JsonResponse({'error': 'El nombre del autor es requerido.'}, status=400)
        nuevo_autor, created = Autor.objects.get_or_create(nombre=nombre)
        if created:
            return JsonResponse({'autor_id': nuevo_autor.id, 'nombre': nuevo_autor.nombre}, status=201)
        else:
            return JsonResponse({'error': 'El autor ya existe.'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)

@login_required
@require_POST
def editar_autor(request, autor_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para editar autores.'}, status=403)
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        nuevo_nombre = data.get('nombre', '').strip()
        if not nuevo_nombre:
            return JsonResponse({'error': 'El nombre del autor no puede estar vacío'}, status=400)
        autor = get_object_or_404(Autor, id=autor_id)
        autor.nombre = nuevo_nombre
        autor.save()
        return JsonResponse({'mensaje': 'Autor actualizado correctamente'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)

@login_required
@require_POST
def eliminar_autor(request, autor_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para eliminar autores.'}, status=403)
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        autor = get_object_or_404(Autor, id=autor_id)
        autor.delete()
        return JsonResponse({'mensaje': 'Autor eliminado correctamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def buscar_autores(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        query = request.GET.get('q', '')
        autores = Autor.objects.filter(Q(nombre__icontains=query))[:10]
        resultados = [{'id': autor.id, 'text': autor.nombre} for autor in autores]
        return JsonResponse({'results': resultados})
    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Vistas para Libros
@login_required
def obtener_libros(request):
    libros = Libro.objects.prefetch_related('autores').all()
    data = [
        {
            'id': libro.id,
            'titulo': libro.titulo,
            'autores_nombres': ", ".join([autor.nombre for autor in libro.autores.all()]),
            'anio_publicacion': libro.anio_publicacion,
            'idioma': libro.idioma,
        }
        for libro in libros
    ]
    return JsonResponse({'data': data})

@login_required
def obtener_libro(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    autores = libro.autores.all()
    data = {
        'id': libro.id,
        'titulo': libro.titulo,
        'anio_publicacion': libro.anio_publicacion,
        'idioma': libro.idioma,
        'autores': [{'id': autor.id, 'nombre': autor.nombre} for autor in autores],
    }
    return JsonResponse(data)

@login_required
@require_POST
def agregar_libro(request):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        titulo = data.get('titulo', '').strip()
        anio_publicacion = data.get('anio_publicacion')
        idioma = data.get('idioma', '').strip()
        autor_ids = data.get('autores', [])
        if not (titulo and anio_publicacion and idioma and autor_ids):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)
        autores = Autor.objects.filter(id__in=autor_ids)
        if not autores.exists():
            return JsonResponse({'error': 'Selecciona al menos un autor válido'}, status=400)
        libro = Libro.objects.create(titulo=titulo, anio_publicacion=anio_publicacion, idioma=idioma)
        libro.autores.set(autores)
        return JsonResponse({'mensaje': 'Libro agregado correctamente'}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)

@login_required
@require_POST
def editar_libro(request, libro_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para editar libros.'}, status=403)
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        titulo = data.get('titulo', '').strip()
        anio_publicacion = data.get('anio_publicacion')
        idioma = data.get('idioma', '').strip()
        autor_ids = data.get('autores', [])
        if not (titulo and anio_publicacion and idioma and autor_ids):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)
        autores = Autor.objects.filter(id__in=autor_ids)
        if not autores.exists():
            return JsonResponse({'error': 'Selecciona al menos un autor válido'}, status=400)
        libro = get_object_or_404(Libro, id=libro_id)
        libro.titulo = titulo
        libro.anio_publicacion = anio_publicacion
        libro.idioma = idioma
        libro.autores.set(autores)
        libro.save()
        return JsonResponse({'mensaje': 'Libro actualizado correctamente'})
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)

@login_required
@require_POST
def eliminar_libro(request, libro_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para eliminar libros.'}, status=403)
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        libro = get_object_or_404(Libro, id=libro_id)
        libro.delete()
        return JsonResponse({'mensaje': 'Libro eliminado correctamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Vistas para Comentarios
@login_required
def obtener_comentarios(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)
    comentarios = libro.comentarios.all().values('id', 'usuario__username', 'texto', 'fecha')
    return JsonResponse(list(comentarios), safe=False)

@login_required
@require_POST
def agregar_comentario(request, libro_id):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    try:
        data = json.loads(request.body)
        texto = data.get("texto", "").strip()
        if texto:
            libro = get_object_or_404(Libro, id=libro_id)
            comentario = Comentario.objects.create(libro=libro, usuario=request.user, texto=texto)
            return JsonResponse({
                'mensaje': 'Comentario agregado correctamente',
                'comentario': {
                    'id': comentario.id,
                    'usuario__username': comentario.usuario.username,
                    'texto': comentario.texto,
                    'fecha': comentario.fecha.strftime('%Y-%m-%d %H:%M'),
                }
            }, status=201)
        return JsonResponse({'error': 'El comentario no puede estar vacío.'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)

@login_required
@require_POST
def editar_comentario(request, comentario_id):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.usuario != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para editar este comentario.'}, status=403)
    try:
        data = json.loads(request.body)
        nuevo_texto = data.get('texto', '').strip()
        if nuevo_texto:
            comentario.texto = nuevo_texto
            comentario.save()
            return JsonResponse({'mensaje': 'Comentario actualizado correctamente'})
        return JsonResponse({'error': 'El texto del comentario no puede estar vacío'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Datos inválidos.'}, status=400)

@login_required
@require_POST
def eliminar_comentario(request, comentario_id):
    if request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    comentario = get_object_or_404(Comentario, id=comentario_id)
    if comentario.usuario != request.user and not request.user.is_staff:
        return JsonResponse({'error': 'No tienes permiso para eliminar este comentario.'}, status=403)
    try:
        comentario.delete()
        return JsonResponse({'mensaje': 'Comentario eliminado correctamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

# Nueva Vista para Obtener Todos los Comentarios
@login_required
def obtener_todos_comentarios(request):
    comentarios = Comentario.objects.select_related('libro', 'usuario').all().values(
        'id', 'libro__titulo', 'usuario__username', 'texto', 'fecha'
    )
    return JsonResponse(list(comentarios), safe=False)


from django.shortcuts import render

def acerca(request):
    return render(request, 'mi_app/acerca_de.html')

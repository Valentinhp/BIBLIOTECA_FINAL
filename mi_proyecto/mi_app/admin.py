# Importa el módulo 'admin' de Django para gestionar el panel de administración
from django.contrib import admin

# Importa los modelos desde el archivo models.py
from .models import Autor, Libro, Comentario

# Configura el panel de administración para los modelos
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')  # Muestra el ID y el nombre en la lista
    search_fields = ('nombre',)  # Permite buscar autores por nombre


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'mostrar_autores', 'anio_publicacion', 'idioma')  # Campos a mostrar
    search_fields = ('titulo', 'autores__nombre')  # Búsqueda por título y autores
    list_filter = ('anio_publicacion', 'idioma')  # Filtros por año de publicación y idioma

    def mostrar_autores(self, obj):
        # Devuelve una lista de autores como un string separado por comas
        return ", ".join([autor.nombre for autor in obj.autores.all()])
    mostrar_autores.short_description = 'Autores'  # Nombre que aparecerá en el admin


@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'libro', 'usuario', 'texto', 'fecha')  # Campos a mostrar
    search_fields = ('libro__titulo', 'usuario__username', 'texto')  # Permite buscar por libro, usuario o texto
    list_filter = ('fecha',)  # Filtro lateral por fecha
    ordering = ('-fecha',)  # Ordena por fecha descendente

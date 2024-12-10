# Importa el módulo 'admin' de Django para gestionar el panel de administración
from django.contrib import admin

# Importa los modelos desde el archivo models.py del mismo directorio
from .models import Autor, Libro, Comentario

# Configura el panel de administración para el modelo 'Autor'
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    # Define los campos que se mostrarán en la lista de autores en el panel de administración
    list_display = ('id', 'nombre')  # Muestra el ID y el nombre del autor en cada fila de la lista
    
    # Define los campos por los cuales se puede buscar en la lista de autores
    search_fields = ('nombre',)  # Permite buscar autores utilizando su nombre

# Configura el panel de administración para el modelo 'Libro'
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    # Define los campos que se mostrarán en la lista de libros en el panel de administración
    list_display = ('id', 'titulo', 'mostrar_autores', 'anio_publicacion', 'idioma')  
    # 'mostrar_autores' es un método personalizado que mostrará los nombres de los autores
    
    # Define los campos por los cuales se puede buscar en la lista de libros
    search_fields = ('titulo', 'autores__nombre')  
    # Permite buscar libros utilizando su título o el nombre de sus autores
    
    # Define los filtros laterales disponibles para refinar la lista de libros
    list_filter = ('anio_publicacion', 'idioma')  
    # Permite filtrar los libros por año de publicación e idioma
    
    # Define la ordenación predeterminada de los libros en la lista
    ordering = ('-anio_publicacion',)  
    # Ordena los libros por año de publicación de forma descendente (del más reciente al más antiguo)
    
    def mostrar_autores(self, obj):
        """
        Método personalizado para mostrar los nombres de los autores de un libro.
        
        Args:
            obj (Libro): Instancia del modelo Libro.
        
        Returns:
            str: Nombres de los autores separados por comas.
        """
        # Obtiene todos los autores relacionados con el libro y concatena sus nombres separados por comas
        return ", ".join([autor.nombre for autor in obj.autores.all()])
    
    # Establece una descripción amigable para la columna 'mostrar_autores' en el panel de administración
    mostrar_autores.short_description = 'Autores'

# Configura el panel de administración para el modelo 'Comentario'
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    # Define los campos que se mostrarán en la lista de comentarios en el panel de administración
    list_display = ('id', 'libro', 'usuario', 'texto', 'fecha')  
    # Muestra el ID del comentario, el libro al que pertenece, el usuario que lo hizo, el texto del comentario y la fecha
    
    # Define los campos por los cuales se puede buscar en la lista de comentarios
    search_fields = ('libro__titulo', 'usuario__username', 'texto')  
    # Permite buscar comentarios utilizando el título del libro, el nombre de usuario o el texto del comentario
    
    # Define los filtros laterales disponibles para refinar la lista de comentarios
    list_filter = ('fecha',)  
    # Permite filtrar los comentarios por fecha
    
    # Define la ordenación predeterminada de los comentarios en la lista
    ordering = ('-fecha',)  
    # Ordena los comentarios por fecha de creación de forma descendente (del más reciente al más antiguo)

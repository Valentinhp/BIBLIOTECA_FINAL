# mi_app/models.py

# Importa el módulo 'models' de Django para definir los modelos de la base de datos
from django.db import models

# Importa el modelo 'User' del módulo de autenticación de Django para relacionarlo con los comentarios
from django.contrib.auth.models import User


class Autor(models.Model):
    """
    Modelo que representa a un Autor en la biblioteca.
    
    Atributos:
        nombre (CharField): Nombre completo del autor. Debe ser único para evitar duplicados.
    """
    nombre = models.CharField(
        max_length=255,  # Define el tamaño máximo del nombre como 255 caracteres
        unique=True  # Asegura que cada nombre de autor sea único en la base de datos
    )  # Campo de texto para el nombre del autor

    def __str__(self):
        """
        Retorna una representación en forma de string del objeto Autor.
        
        Returns:
            str: El nombre del autor.
        """
        return self.nombre  # Retorna el nombre del autor para una representación legible


class Libro(models.Model):
    """
    Modelo que representa a un Libro en la biblioteca.
    
    Atributos:
        titulo (CharField): Título del libro.
        anio_publicacion (PositiveIntegerField): Año de publicación del libro. Es opcional.
        idioma (CharField): Idioma en el que está escrito el libro. Por defecto es 'Español'.
        autores (ManyToManyField): Relación de muchos a muchos con el modelo Autor.
    """
    titulo = models.CharField(
        max_length=255  # Define el tamaño máximo del título como 255 caracteres
    )  # Campo de texto para el título del libro

    anio_publicacion = models.PositiveIntegerField(
        null=True,  # Permite que el campo sea nulo en la base de datos
        blank=True  # Permite que el campo sea opcional en formularios
    )  # Campo numérico para el año de publicación, solo números positivos

    idioma = models.CharField(
        max_length=100,  # Define el tamaño máximo del idioma como 100 caracteres
        default='Español'  # Establece 'Español' como valor por defecto
    )  # Campo de texto para el idioma del libro

    autores = models.ManyToManyField(
        Autor,  # Relación con el modelo Autor
        related_name='libros'  # Nombre inverso para acceder a los libros desde un autor
    )  # Relación de muchos a muchos con autores

    def __str__(self):
        """
        Retorna una representación en forma de string del objeto Libro.
        
        Returns:
            str: El título del libro.
        """
        return self.titulo  # Retorna el título del libro para una representación legible


class Comentario(models.Model):
    """
    Modelo que representa un Comentario realizado por un Usuario sobre un Libro.
    
    Atributos:
        libro (ForeignKey): Relación de muchos a uno con el modelo Libro.
        usuario (ForeignKey): Relación de muchos a uno con el modelo User.
        texto (TextField): Texto del comentario.
        fecha (DateTimeField): Fecha y hora en que se creó el comentario.
    """
    libro = models.ForeignKey(
        Libro,  # Relación con el modelo Libro
        on_delete=models.CASCADE,  # Elimina el comentario si se elimina el libro asociado
        related_name='comentarios'  # Nombre inverso para acceder a los comentarios desde un libro
    )  # Relación de muchos a uno con el libro comentado

    usuario = models.ForeignKey(
        User,  # Relación con el modelo User de Django
        on_delete=models.CASCADE,  # Elimina el comentario si se elimina el usuario asociado
        related_name='comentarios'  # Nombre inverso para acceder a los comentarios desde un usuario
    )  # Relación de muchos a uno con el usuario que hizo el comentario

    texto = models.TextField()  # Campo de texto para el contenido del comentario

    fecha = models.DateTimeField(
        auto_now_add=True  # Establece automáticamente la fecha y hora al crear el comentario
    )  # Campo de fecha y hora para cuándo se creó el comentario

    def __str__(self):
        """
        Retorna una representación en forma de string del objeto Comentario.
        
        Returns:
            str: Una cadena que indica quién hizo el comentario y sobre qué libro.
        """
        return f'Comentario de {self.usuario.username} en {self.libro.titulo}'
        # Retorna una descripción legible del comentario, indicando el usuario y el libro asociado

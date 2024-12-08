# mi_app/models.py
from django.db import models
from django.contrib.auth.models import User

class Autor(models.Model):
    nombre = models.CharField(max_length=255, unique=True)  # Evita duplicados

    def __str__(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    anio_publicacion = models.PositiveIntegerField(null=True, blank=True)  # Para permitir años opcionales
    idioma = models.CharField(max_length=100, default='Español')
    autores = models.ManyToManyField(Autor, related_name='libros')

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='comentarios')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios')
    texto = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentario de {self.usuario.username} en {self.libro.titulo}'

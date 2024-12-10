# mi_app/management/commands/import_libros.py

import csv  # Importa el módulo CSV para leer archivos CSV
import os  # Importa el módulo OS para interactuar con el sistema operativo
from django.core.management.base import BaseCommand  # Importa la clase base para comandos de gestión personalizados
from mi_app.models import Autor, Libro  # Importa los modelos Autor y Libro de tu aplicación

class Command(BaseCommand):
    help = "Importa datos de libros desde un archivo CSV"  # Define una breve descripción del comando
    
    # Ruta fija al archivo CSV
    CSV_FILE_PATH = r"C:\Users\Valen\Downloads\ENTORNOS\ENTORNO_4_NOV\ENTORNO_4_NOV\ENTORNO_4_NOV\mi_proyecto\mi_app\management\commands\data\BD_LIBRERIA.csv"
    
    def handle(self, *args, **kwargs):
        """
        Método principal que se ejecuta al llamar al comando.
        Maneja la lógica de importación de datos desde el archivo CSV.
        """
        # Verificar si el archivo existe
        if not os.path.exists(self.CSV_FILE_PATH):
            self.stderr.write(f"El archivo {self.CSV_FILE_PATH} no existe. Verifica la ruta.")  # Muestra un mensaje de error si el archivo no existe
            return  # Termina la ejecución del comando
        
        # Leer el archivo CSV
        with open(self.CSV_FILE_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)  # Crea un lector de CSV que devuelve cada fila como un diccionario
            for row in reader:
                # Convertir anio_publicacion a entero, si es posible
                try:
                    anio_publicacion = int(float(row.get('Publication_Year', 0)))  # Intenta convertir el año de publicación a entero
                except ValueError:
                    anio_publicacion = None  # Asigna None si la conversión falla
                
                # Crear o recuperar autores
                autor_nombres = row['Authors'].split(", ")  # Divide los nombres de autores separados por comas y espacios
                autores = []  # Inicializa una lista para almacenar los objetos Autor
                for autor_nombre in autor_nombres:
                    autor, created = Autor.objects.get_or_create(nombre=autor_nombre)  # Obtiene o crea un Autor con el nombre dado
                    autores.append(autor)  # Añade el Autor a la lista de autores
                
                # Crear libro
                libro, created = Libro.objects.get_or_create(
                    titulo=row['Title'],  # Título del libro desde el CSV
                    anio_publicacion=anio_publicacion,  # Año de publicación convertido previamente
                    idioma=row.get('language_code', 'eng'),  # Código de idioma, por defecto 'eng' si no está presente
                    calificacion_promedio=row.get('average_rating', 0.0),  # Calificación promedio, por defecto 0.0
                    total_calificaciones=row.get('Ratings_Count', 0),  # Total de calificaciones, por defecto 0
                    reseñas_texto=row.get('Text_Reviews', 0),  # Reseñas de texto, por defecto 0
                )
                
                # Asociar autores al libro
                libro.autores.set(autores)  # Asocia la lista de autores al libro
                libro.save()  # Guarda los cambios en la base de datos
                
                # Mostrar mensaje de éxito en la consola
                self.stdout.write(f"Libro '{libro.titulo}' importado correctamente.")

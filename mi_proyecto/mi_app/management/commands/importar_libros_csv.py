import csv
import os
from django.core.management.base import BaseCommand
from mi_app.models import Autor, Libro

class Command(BaseCommand):
    help = "Importa datos de libros desde un archivo CSV"

    # Ruta fija al archivo CSV
    CSV_FILE_PATH = r"C:\Users\Valen\Downloads\ENTORNOS\ENTORNO_4_NOV\ENTORNO_4_NOV\ENTORNO_4_NOV\mi_proyecto\mi_app\management\commands\data\BD_LIBRERIA.csv"

    def handle(self, *args, **kwargs):
        # Verificar si el archivo existe
        if not os.path.exists(self.CSV_FILE_PATH):
            self.stderr.write(f"El archivo {self.CSV_FILE_PATH} no existe. Verifica la ruta.")
            return

        # Leer el archivo CSV
        with open(self.CSV_FILE_PATH, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convertir anio_publicacion a entero, si es posible
                try:
                    anio_publicacion = int(float(row.get('Publication_Year', 0)))
                except ValueError:
                    anio_publicacion = None  # Valor por defecto si no es un número

                # Crear o recuperar autores
                autor_nombres = row['Authors'].split(", ")
                autores = []
                for autor_nombre in autor_nombres:
                    autor, created = Autor.objects.get_or_create(nombre=autor_nombre)
                    autores.append(autor)

                # Crear libro
                libro, created = Libro.objects.get_or_create(
                    titulo=row['Title'],
                    anio_publicacion=anio_publicacion,
                    idioma=row.get('language_code', 'eng'),
                    calificacion_promedio=row.get('average_rating', 0.0),
                    total_calificaciones=row.get('Ratings_Count', 0),
                    reseñas_texto=row.get('Text_Reviews', 0),
                )
                # Asociar autores al libro
                libro.autores.set(autores)
                libro.save()
                self.stdout.write(f"Libro '{libro.titulo}' importado correctamente.")

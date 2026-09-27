import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Genre, Movie

def translate():
    genre_translations = {
        'Action': 'Acción',
        'Comedy': 'Comedia',
        'Drama': 'Drama',
        'Science Fiction': 'Ciencia Ficción'
    }

    for eng, esp in genre_translations.items():
        Genre.objects.filter(name=eng).update(name=esp)
    print("Genres translated.")

    movies = Movie.objects.all()
    for m in movies:
        m.description = f"Una excelente producción cinematográfica titulada {m.title}, estrenada en el año {m.release_year}."
        m.save()
    print("Movie descriptions translated to Spanish.")

if __name__ == '__main__':
    translate()

import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Movie

def assign_posters():
    mapping = {
        "Step Brothers": r"C:\Users\farid\Downloads\Step Brothers.jpg",
        "Anchorman: The Legend of Ron Burgundy": r"C:\Users\farid\Downloads\Anchorman.jpg"
    }

    for title, path in mapping.items():
        movie = Movie.objects.filter(title=title).first()
        if movie and os.path.exists(path):
            with open(path, 'rb') as f:
                movie.poster.save(f"poster_{movie.id}.jpg", File(f), save=True)
            print(f"Assigned user poster to: {title}")
        else:
            print(f"Could not find movie {title} or file {path}")

if __name__ == '__main__':
    assign_posters()

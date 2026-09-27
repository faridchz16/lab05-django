import os
import django
import urllib.request
from django.core.files import File
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Movie

def set_poster():
    movie = Movie.objects.filter(title="Step Brothers").first()
    if not movie:
        return

    urls = [
        "https://upload.wikimedia.org/wikipedia/en/1/18/Step_Brothers_Poster.jpg",
        "https://upload.wikimedia.org/wikipedia/en/7/77/Step_brothers.jpg",
        "https://upload.wikimedia.org/wikipedia/en/thumb/d/d4/Stepbrothersthemovie.jpg/220px-Stepbrothersthemovie.jpg"
    ]
    headers = {'User-Agent': 'Mozilla/5.0'}

    for u in urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                movie.poster.save(f"poster_{movie.id}.jpg", File(BytesIO(resp.read())), save=True)
                print(f"Success with {u}")
                return
        except Exception as e:
            print(f"Failed {u}: {e}")

if __name__ == '__main__':
    set_poster()

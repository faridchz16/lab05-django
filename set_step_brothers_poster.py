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
        print("Movie not found")
        return

    urls = [
        "https://upload.wikimedia.org/wikipedia/en/d/d4/Stepbrothersthemovie.jpg",
        "https://upload.wikimedia.org/wikipedia/en/1/1c/Step_Brothers_%282008%29_theatrical_poster.jpg",
        "https://m.media-amazon.com/images/M/MV5BODIxMjE0MTY4Ml5BMl5BanBnXkFtZTcwMTA1MTQzMw@@._V1_SY1000_CR0,0,675,1000_AL_.jpg",
        "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=800&auto=format&fit=crop"
    ]

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    for url in urls:
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                img_io = BytesIO(response.read())
                movie.poster.save(f"poster_{movie.id}.jpg", File(img_io), save=True)
                print(f"Successfully set Step Brothers poster from: {url}")
                return
        except Exception as e:
            print(f"Tried {url} -> Failed: {e}")

if __name__ == '__main__':
    set_poster()

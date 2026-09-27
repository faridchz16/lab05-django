import os
import django
import urllib.request
import time
from django.core.files import File
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Movie

POSTER_URLS = {
    "Jurassic Park": "https://upload.wikimedia.org/wikipedia/en/e/e7/Jurassic_Park_poster.jpg",
    "Superbad": "https://upload.wikimedia.org/wikipedia/en/8/8b/Superbad_Poster.png",
}

def download_posters():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    for movie_title, url in POSTER_URLS.items():
        try:
            movie = Movie.objects.filter(title=movie_title).first()
            if not movie:
                print(f"Movie not found in DB: {movie_title}")
                continue
            
            time.sleep(2)
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                image_data = response.read()
                image_io = BytesIO(image_data)
                ext = url.split('.')[-1].lower()
                if '?' in ext:
                    ext = ext.split('?')[0]
                if ext not in ['jpg', 'jpeg', 'png']:
                    ext = 'jpg'
                movie.poster.save(f"poster_{movie.id}.{ext}", File(image_io), save=True)
                print(f"Successfully downloaded real poster for: {movie_title}")
        except Exception as e:
            print(f"Failed to download poster for {movie_title}: {e}")

if __name__ == '__main__':
    download_posters()

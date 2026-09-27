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

    # Try a known TMDb/IMDb CDN image URL for Step Brothers
    url = "https://m.media-amazon.com/images/M/MV5BMTM3MjQwMTI5OV5BMl5BanBnXkFtZTcwNTgyNTk3OA@@._V1_FMjpg_UX1000_.jpg"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as response:
            img_io = BytesIO(response.read())
            movie.poster.save(f"poster_{movie.id}.jpg", File(img_io), save=True)
            print("Successfully set Step Brothers poster from Amazon/IMDb CDN!")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == '__main__':
    set_poster()

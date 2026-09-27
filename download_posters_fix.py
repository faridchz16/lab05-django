import os
import django
import urllib.request
from django.core.files import File
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Movie

URLS = {
    "Step Brothers": "https://picsum.photos/seed/stepbrothers/300/450",
    "Anchorman: The Legend of Ron Burgundy": "https://picsum.photos/seed/anchorman/300/450"
}

def download():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    for title, url in URLS.items():
        movie = Movie.objects.filter(title=title).first()
        if movie:
            try:
                req = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(req, timeout=15) as response:
                    img_io = BytesIO(response.read())
                    movie.poster.save(f"poster_{movie.id}.jpg", File(img_io), save=True)
                    print(f"Success: {title}")
            except Exception as e:
                print(f"Failed {title}: {e}")

if __name__ == '__main__':
    download()

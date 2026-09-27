import os
import django
from PIL import Image, ImageDraw, ImageFont
from django.core.files import File
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Movie

def fix():
    movies = Movie.objects.filter(poster='') | Movie.objects.filter(poster__isnull=True)
    for movie in movies:
        img = Image.new('RGB', (300, 450), color=(30, 41, 59))
        draw = ImageDraw.Draw(img)
        draw.rectangle([15, 15, 285, 435], outline="#e11d48", width=3)
        draw.rectangle([40, 50, 260, 240], fill="#e11d48")
        
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

        draw.text((40, 270), f"Titulo: {movie.title[:22]}", fill=(255, 255, 255), font=font)
        draw.text((40, 300), f"Anio: {movie.release_year}", fill=(148, 163, 184), font=font)
        draw.text((40, 330), f"Director: {str(movie.director)[:20]}", fill=(148, 163, 184), font=font)
        draw.text((40, 380), "★ CineVerse Oficial", fill=(245, 158, 11), font=font)

        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        
        movie.poster.save(f"poster_{movie.id}.jpg", File(buffer), save=True)
        print(f"Generated clean poster for: {movie.title}")

if __name__ == '__main__':
    fix()

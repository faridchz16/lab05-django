import os
import django
from PIL import Image, ImageDraw, ImageFont
from django.core.files import File
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Movie

def generate():
    movies = Movie.objects.all()
    color_schemes = [
        ("#e11d48", "#1e293b"), # Red / Slate
        ("#3b82f6", "#0f172a"), # Blue / Dark
        ("#f59e0b", "#18181b"), # Gold / Zinc
        ("#10b981", "#022c22"), # Emerald / Dark Green
        ("#8b5cf6", "#2e1065"), # Purple / Deep Indigo
    ]
    
    for idx, movie in enumerate(movies):
        accent_color, base_color = color_schemes[idx % len(color_schemes)]
        
        # Create image 300x450
        img = Image.new('RGB', (300, 450), color=base_color)
        draw = ImageDraw.Draw(img)
        
        # Draw decorative border
        draw.rectangle([15, 15, 285, 435], outline=accent_color, width=3)
        
        # Draw central accent box representing poster art
        draw.rectangle([40, 50, 260, 240], fill=accent_color)
        
        # Draw text details
        text = movie.title
        year = str(movie.release_year)
        director = str(movie.director) if movie.director else "Unknown"

        try:
            font = ImageFont.load_default()
        except Exception:
            font = None

        draw.text((40, 270), f"Title: {text}", fill=(255, 255, 255), font=font)
        draw.text((40, 300), f"Year: {year}", fill=(148, 163, 184), font=font)
        draw.text((40, 330), f"Director: {director}", fill=(148, 163, 184), font=font)
        draw.text((40, 380), "★ CineVerse Official", fill=(245, 158, 11), font=font)

        buffer = BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)
        
        movie.poster.save(f"poster_{movie.id}.jpg", File(buffer), save=True)
        print(f"Generated professional poster for: {movie.title}")

if __name__ == '__main__':
    generate()

import os
import django
import urllib.request
import time
from django.core.files import File
from io import BytesIO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Genre, Person, Movie, Rating

NEW_MOVIES = [
    {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "director_fn": "Frank",
        "director_ln": "Darabont",
        "genres": ["Drama"],
        "poster_url": "https://upload.wikimedia.org/wikipedia/en/8/81/ShawshankRedemptionMoviePoster.jpg",
        "description": "Acusado injustamente del asesinato de su esposa y su amante, Andy Dufresne es condenado a cadena perpetua en la penitenciaría de Shawshank. A lo largo de dos décadas, su ingenio, dignidad inquebrantable y una profunda amistad con el contrabandista Red transforman las vidas de los reclusos y desafían la brutalidad del sistema penitenciario.",
        "ratings": [
            ("IMDb_Critic", 9, "Considerada por millones como la mejor película de la historia del cine."),
            ("Rotten_Tomatoes", 9, "Una obra maestra conmovedora sobre la esperanza y la redención humana."),
            ("Empire", 9, "Dirección impecable y actuaciones legendarias de Tim Robbins y Morgan Freeman.")
        ]
    },
    {
        "title": "Fight Club",
        "year": 1999,
        "director_fn": "David",
        "director_ln": "Fincher",
        "genres": ["Drama"],
        "poster_url": "https://upload.wikimedia.org/wikipedia/en/f/fc/Fight_Club_poster.jpg",
        "description": "Un empleado de oficina insomne y hastiado de su rutinario consumismo moderno conoce a Tyler Durden, un carismático vendedor de jabón con una filosofía nihilista. Juntos fundan un club de lucha clandestino que evoluciona rápidamente hacia un movimiento subversivo y caótico de escala nacional.",
        "ratings": [
            ("IMDb_Critic", 9, "Un thriller psicológico audaz, oscuro y de profunda crítica social."),
            ("Rolling_Stone", 8, "Una descarga eléctrica de furia generacional y estilo visual deslumbrante."),
            ("Sight_&_Sound", 8, "Una sátira feroz sobre la masculinidad y el capitalismo moderno.")
        ]
    },
    {
        "title": "Forrest Gump",
        "year": 1994,
        "director_fn": "Robert",
        "director_ln": "Zemeckis",
        "genres": ["Drama"],
        "poster_url": "https://upload.wikimedia.org/wikipedia/en/6/67/Forrest_Gump_poster.jpg",
        "description": "La extraordinaria y entrañable vida de Forrest Gump, un hombre bondadoso de baja estatura intelectual que, sin proponérselo, participa en momentos cruciales de la historia contemporánea de Estados Unidos, mientras su corazón permanece eternamente devoto a su amor de infancia, Jenny.",
        "ratings": [
            ("Academy_Awards", 9, "Ganadora de 6 premios Óscar incluyendo Mejor Película y Mejor Actor para Tom Hanks."),
            ("Chicago_Sun_Times", 9, "Un cuento de hadas moderno lleno de magia, emoción y nostalgia inolvidable."),
            ("Variety", 8, "Una hazaña narrativa y técnica conmovedora que cautivó al mundo entero.")
        ]
    },
    {
        "title": "The Hangover",
        "year": 2009,
        "director_fn": "Todd",
        "director_ln": "Phillips",
        "genres": ["Comedia"],
        "poster_url": "https://upload.wikimedia.org/wikipedia/en/b/b9/Hangoverposter09.jpg",
        "description": "Tres amigos despiertan en una suite de Las Vegas tras una salvaje despedida de soltero sin recordar absolutamente nada. Con un tigre en el baño, un bebé en el armario y el novio desaparecido pocas horas antes de su boda, deben reconstruir las pistas de su caótica noche anterior.",
        "ratings": [
            ("IMDb_Critic", 8, "Una de las comedias más desternillantes, taquilleras e influyentes del siglo XXI."),
            ("Hollywood_Reporter", 8, "Ritmo cómico frenético y química perfecta entre su elenco estelar."),
            ("Empire", 7, "Impredecible, vulgar y sumamente divertida de principio a fin.")
        ]
    },
    {
        "title": "Step Brothers",
        "year": 2008,
        "director_fn": "Adam",
        "director_ln": "McKay",
        "genres": ["Comedia"],
        "poster_url": "https://upload.wikimedia.org/wikipedia/en/d/d4/Stepbrothersthemovie.jpg",
        "description": "Brennan y Dale son dos hombres maduros de cuarenta años que aún viven con sus respectivos padres inmaduros. Cuando sus padres se casan y deciden vivir juntos, ambos se ven obligados a compartir habitación, declarándose una guerra absurda y delirante antes de convertirse en mejores amigos inseparables.",
        "ratings": [
            ("IMDb_Critic", 7, "Una joya de la comedia absurda protagonizada por Will Ferrell y John C. Reilly."),
            ("IndieWire", 7, "Improvisación brillante y humor desinhibido sin complejos."),
            ("Rolling_Stone", 7, "Una oda hilarante a la inmadurez adulta que mejora con cada visionado.")
        ]
    },
    {
        "title": "Anchorman: The Legend of Ron Burgundy",
        "year": 2004,
        "director_fn": "Adam",
        "director_ln": "McKay",
        "genres": ["Comedia"],
        "poster_url": "https://upload.wikimedia.org/wikipedia/en/6/64/Anchorman_The_Legend_of_Ron_Burgundy_Poster.jpg",
        "description": "En la década de 1970 en San Diego, Ron Burgundy es el presentador de noticias más respetado y engreído de la televisión. Su mundo machista y dominado por hombres se tambalea por completo cuando la cadena contrata a una ambiciosa y brillante periodista, Veronica Corningstone.",
        "ratings": [
            ("IMDb_Critic", 7, "Una comedia de culto absoluta con frases icónicas y un elenco cómico legendario."),
            ("Variety", 7, "Will Ferrell brilla en su máxima expresión en esta sátira mordaz de los informativos."),
            ("Time_Out", 8, "Descarada, excéntrica y desternillante de principio a fin.")
        ]
    }
]

def add_movies():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36'}
    
    for item in NEW_MOVIES:
        movie, created = Movie.objects.get_or_create(
            title=item["title"],
            defaults={
                'release_year': item["year"],
                'description': item["description"]
            }
        )
        
        # Director
        director, _ = Person.objects.get_or_create(
            first_name=item["director_fn"],
            last_name=item["director_ln"]
        )
        movie.director = director
        
        # Genres
        genre_objs = []
        for g_name in item["genres"]:
            g_obj, _ = Genre.objects.get_or_create(name=g_name)
            genre_objs.append(g_obj)
        movie.genres.set(genre_objs)
        movie.save()
        
        # Ratings
        movie.ratings.all().delete()
        for user, score, comment in item["ratings"]:
            Rating.objects.create(
                movie=movie,
                user_name=user,
                score=score,
                comment=comment
            )
            
        # Download poster
        try:
            time.sleep(1)
            req = urllib.request.Request(item["poster_url"], headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                image_data = response.read()
                image_io = BytesIO(image_data)
                ext = item["poster_url"].split('.')[-1].lower()
                if '?' in ext:
                    ext = ext.split('?')[0]
                if ext not in ['jpg', 'jpeg', 'png']:
                    ext = 'jpg'
                movie.poster.save(f"poster_{movie.id}.{ext}", File(image_io), save=True)
                print(f"Added and downloaded poster for: {item['title']}")
        except Exception as e:
            print(f"Added movie {item['title']} but failed poster download: {e}")

if __name__ == '__main__':
    add_movies()

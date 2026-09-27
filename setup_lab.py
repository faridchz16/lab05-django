import os
import django
import urllib.request
from io import BytesIO
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from movies.models import Genre, Person, Movie, Rating

def run():
    print("Setting up superuser...")
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print("Superuser 'admin' created.")
    else:
        print("Superuser 'admin' already exists.")

    print("Creating test genres...")
    genre_names = ['Action', 'Comedy', 'Drama', 'Science Fiction']
    genres = {}
    for name in genre_names:
        g, created = Genre.objects.get_or_create(name=name)
        genres[name] = g
    
    print("Creating test persons (directors)...")
    directors_data = [
        ('Christopher', 'Nolan'),
        ('Quentin', 'Tarantino'),
        ('Steven', 'Spielberg'),
        ('Denis', 'Villeneuve'),
    ]
    directors = []
    for fn, ln in directors_data:
        p, created = Person.objects.get_or_create(first_name=fn, last_name=ln)
        directors.append(p)

    print("Creating 10 test movies and fetching poster images...")
    movies_data = [
        ("Inception", 2010, directors[0], [genres['Action'], genres['Science Fiction']]),
        ("Interstellar", 2014, directors[0], [genres['Drama'], genres['Science Fiction']]),
        ("Pulp Fiction", 1994, directors[1], [genres['Action'], genres['Drama']]),
        ("Django Unchained", 2012, directors[1], [genres['Action'], genres['Drama']]),
        ("Jurassic Park", 1993, directors[2], [genres['Action'], genres['Science Fiction']]),
        ("Schindler's List", 1993, directors[2], [genres['Drama']]),
        ("Blade Runner 2049", 2017, directors[3], [genres['Drama'], genres['Science Fiction']]),
        ("Arrival", 2016, directors[3], [genres['Drama'], genres['Science Fiction']]),
        ("The Dark Knight", 2008, directors[0], [genres['Action'], genres['Drama']]),
        ("Superbad", 2007, directors[2], [genres['Comedy']]),
    ]

    created_movies = []
    for idx, (title, year, director, movie_genres) in enumerate(movies_data):
        m, created = Movie.objects.get_or_create(
            title=title,
            defaults={'release_year': year, 'director': director, 'description': f"An epic cinematic experience titled {title}, released in {year}."}
        )
        if created:
            m.genres.set(movie_genres)
            # Fetch sample poster image from Picsum Photos
            try:
                seed = title.replace(" ", "")
                url = f"https://picsum.photos/seed/{seed}/300/450"
                req = urllib.request.urlopen(url, timeout=5)
                image_io = BytesIO(req.read())
                m.poster.save(f"movie_{idx+1}.jpg", File(image_io), save=True)
                print(f"Downloaded poster for {title}")
            except Exception as e:
                print(f"Could not download poster for {title}: {e}")
        created_movies.append(m)

    print("Creating ratings for at least 5 movies...")
    for i in range(6):
        m = created_movies[i]
        Rating.objects.get_or_create(
            movie=m,
            user_name=f"Viewer_{i+1}",
            score=8 + (i % 3),
            comment="A brilliant film with outstanding direction and performances!"
        )

    print("Configuring 'editores' group and permissions...")
    editor_group, created = Group.objects.get_or_create(name='editores')
    
    movie_ct = ContentType.objects.get_for_model(Movie)
    genre_ct = ContentType.objects.get_for_model(Genre)
    person_ct = ContentType.objects.get_for_model(Person)
    rating_ct = ContentType.objects.get_for_model(Rating)

    perm_codes = [
        'add_movie', 'change_movie', 'view_movie',
        'view_genre', 'view_person', 'view_rating',
        'add_genre', 'change_genre',
        'add_person', 'change_person',
        'add_rating', 'change_rating',
    ]
    
    permissions = Permission.objects.filter(codename__in=perm_codes, content_type__in=[movie_ct, genre_ct, person_ct, rating_ct])
    editor_group.permissions.set(permissions)

    print("Creating test editor user...")
    if not User.objects.filter(username='editor1').exists():
        editor_user = User.objects.create_user('editor1', 'editor1@example.com', 'editor123')
        editor_user.groups.add(editor_group)
        print("User 'editor1' created and added to 'editores' group.")
    else:
        editor_user = User.objects.get(username='editor1')
        if not editor_user.groups.filter(name='editores').exists():
            editor_user.groups.add(editor_group)
        print("User 'editor1' already exists.")

    print("Setup and image download completed successfully!")

if __name__ == '__main__':
    run()

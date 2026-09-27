import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from movies.models import Movie, Rating

def add_missing_ratings():
    ratings_data = {
        "The Dark Knight": [
            ("Critic_1", 10, "Una obra maestra absoluta del cine moderno."),
            ("Critic_2", 9, "La mejor actuación de Joker y dirección impecable.")
        ],
        "Superbad": [
            ("Critic_1", 8, "Una comedia sumamente divertida e inolvidable."),
            ("Critic_2", 8, "Gran química entre los protagonistas.")
        ],
        "Blade Runner 2049": [
            ("Critic_1", 9, "Visualmente impresionante y con una narrativa profunda."),
            ("Critic_2", 8, "Una secuela digna que expande el universo original.")
        ],
        "Arrival": [
            ("Critic_1", 8, "Ciencia ficción inteligente y conmovedora."),
            ("Critic_2", 9, "Excelente guion y enfoque sobre la comunicación.")
        ]
    }

    for movie_title, reviews in ratings_data.items():
        movie = Movie.objects.filter(title=movie_title).first()
        if movie:
            for user, score, comment in reviews:
                Rating.objects.get_or_create(
                    movie=movie,
                    user_name=user,
                    defaults={'score': score, 'comment': comment}
                )
            print(f"Added ratings for: {movie_title}")

if __name__ == '__main__':
    add_missing_ratings()

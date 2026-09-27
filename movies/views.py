from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from .models import Movie, Genre


def movie_list_view(request):
    movies = Movie.objects.annotate(avg_rating=Avg('ratings__score')).all()
    genres = Genre.objects.all()
    selected_genre = request.GET.get('genre')
    if selected_genre:
        movies = movies.filter(genres__id=selected_genre)
    return render(request, 'movies/movie_list.html', {
        'movies': movies,
        'genres': genres,
        'selected_genre': selected_genre
    })


def movie_recommendation_view(request, movie_id):
    movie = get_object_or_404(Movie.objects.annotate(avg_rating=Avg('ratings__score')), pk=movie_id)
    movie_genres = movie.genres.all()
    
    # Recommend movies sharing same genres, annotated with average rating, excluding current movie
    recommendations = Movie.objects.filter(
        genres__in=movie_genres
    ).exclude(
        pk=movie.pk
    ).annotate(
        avg_rating=Avg('ratings__score')
    ).distinct().order_by('-avg_rating', '-release_year')[:5]

    return render(request, 'movies/movie_recommendation.html', {
        'movie': movie,
        'recommendations': recommendations
    })

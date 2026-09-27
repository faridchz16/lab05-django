from django.urls import path
from .views import movie_list_view, movie_recommendation_view

app_name = 'movies'

urlpatterns = [
    path('', movie_list_view, name='movie_list'),
    path('recommendation/<int:movie_id>/', movie_recommendation_view, name='movie_recommendation'),
]

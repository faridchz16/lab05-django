from django.contrib import admin
from .models import Genre, Person, Movie, Rating


class RatingInline(admin.TabularInline):
    model = Rating
    extra = 1
    readonly_fields = ('created_at',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'birth_date')
    search_fields = ('first_name', 'last_name')
    list_filter = ('birth_date',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'release_year', 'director', 'display_genres', 'created_at')
    list_filter = ('release_year', 'genres')
    search_fields = ('title', 'director__first_name', 'director__last_name')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RatingInline]
    filter_horizontal = ('genres',)

    def display_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genres.all()])
    display_genres.short_description = 'Genres'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user_name', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('user_name', 'movie__title')
    readonly_fields = ('created_at',)

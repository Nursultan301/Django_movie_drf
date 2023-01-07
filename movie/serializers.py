from rest_framework import serializers

from movie.models import Movie


class MovieListSerializers(serializers.ModelSerializer):
    """ Список фильмов """

    class Meta:
        model = Movie
        fields = ["title", 'tagline', 'category']


class MovieDetailSerializers(serializers.ModelSerializer):
    """ Полный описание фильмов """
    category = serializers.SlugRelatedField(slug_field="title", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="title", read_only=True, many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)

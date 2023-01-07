from rest_framework import serializers

from movie.models import Movie, Review


class MovieListSerializers(serializers.ModelSerializer):
    """ Список фильмов """

    class Meta:
        model = Movie
        fields = ["title", 'tagline', 'category']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """ Добавление отзыва """

    class Meta:
        model = Review
        fields = '__all__'


class FilterReviewListSerializer(serializers.ListSerializer):
    """ Фильтр комментариев, только parents """

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):
    """Вывод рекурсию children"""

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ReviewSerializer(serializers.ModelSerializer):
    """ Вывод отзыва """
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ('name', "text", "children")


class MovieDetailSerializers(serializers.ModelSerializer):
    """ Полный описание фильмов """
    category = serializers.SlugRelatedField(slug_field="title", read_only=True)
    directors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    actors = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="title", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)

from rest_framework import serializers

from movie.models import Movie, Review, Rating, Actor


class MovieListSerializers(serializers.ModelSerializer):
    """ Список фильмов """
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

    class Meta:
        model = Movie
        fields = ["id", "title", "tagline", "category", "rating_user", "middle_star"]


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


class ActorListSerializer(serializers.ModelSerializer):
    """ Вывод списка актеров и режиссеров """

    class Meta:
        model = Actor
        fields = ('id', 'name', 'image')


class ActorDetailSerializer(serializers.ModelSerializer):
    """ Вывод полного описание актера и режиссеров """

    class Meta:
        model = Actor
        fields = "__all__"


class MovieDetailSerializers(serializers.ModelSerializer):
    """ Полный описание фильмов """
    category = serializers.SlugRelatedField(slug_field="title", read_only=True)
    directors = ActorListSerializer(read_only=True, many=True)
    actors = ActorListSerializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="title", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('draft',)


class CreateRatingSerializer(serializers.ModelSerializer):
    """ Добавление рейтинга пользователем """

    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={'star': validated_data.get('star')}
        )
        return rating

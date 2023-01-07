from django.db import models
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    MovieListSerializers,
    MovieDetailSerializers,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSerializer, ActorDetailSerializer
)
from .service import get_client_ip, MovieFilter


class MovieListView(generics.ListAPIView):
    """ Вывод списка фильмов """
    serializer_class = MovieListSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MovieFilter

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    """ Вывод фильма """
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializers


class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewCreateSerializer


class AddStarRatingView(generics.CreateAPIView):
    """ Добавление рейтинга фильму """
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        serializer.save(ip=get_client_ip(self.request))


class ActorsListView(generics.ListAPIView):
    """Вывод списка актеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    """Вывод списка актеров"""
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer

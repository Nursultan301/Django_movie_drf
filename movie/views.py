from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie
from .serializers import MovieListSerializers, MovieDetailSerializers


class MovieListView(APIView):
    """ Вывод списка фильмов """
    def get(self, request):
        movies = Movie.objects.filter(draft=False)
        serializer = MovieListSerializers(movies, many=True)
        return Response(serializer.data)


class MovieDetailView(APIView):
    """ Вывод фильма """
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializers(movie)
        return Response(serializer.data)

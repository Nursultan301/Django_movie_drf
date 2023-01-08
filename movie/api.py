from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response

from movie.models import Actor
from movie.serializers import ActorListSerializer, ActorDetailSerializer


class ActorViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Actor.objects.all()
        serializer = ActorListSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Actor.objects.all()
        actor = get_object_or_404(queryset, pk=pk)
        serializer = ActorDetailSerializer(actor)
        return Response(serializer.data)



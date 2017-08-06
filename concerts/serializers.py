from rest_framework import serializers
from .models import ConcertsGenre, ConcertsEvent


class ConcertsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConcertsEvent
        fields = ('name', 'description')


class ConcertsGenreSerializer(serializers.ModelSerializer):
    events = ConcertsEventSerializer(many=True, read_only=True)

    class Meta:
        model = ConcertsGenre
        fields = ('name', 'description', 'events')

from rest_framework import serializers
from .models import ArtsAndIdeasGenre, ArtsAndIdeasEvent


class ArtsAndIdeasEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtsAndIdeasEvent
        fields = ('name', 'description')


class ArtsAndIdeasGenreSerializer(serializers.ModelSerializer):
    events = ArtsAndIdeasEventSerializer(many=True, read_only=True)

    class Meta:
        model = ArtsAndIdeasGenre
        fields = ('name', 'description', 'events')

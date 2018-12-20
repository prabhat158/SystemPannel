from rest_framework import serializers
from .models import InformalsEvent, InformalsGenre


class InformalsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformalsEvent
        fields = ('name', 'description', 'image', 'link')


class InformalsGenreSerializer(serializers.ModelSerializer):
    events = InformalsEventSerializer(many=True, read_only=True)

    class Meta:
        model = InformalsGenre
        fields = ('name', 'description', 'events')

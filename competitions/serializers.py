from rest_framework import serializers
from .models import CompetitionsEvent, CompetitionsGenre


class CompetitionsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionsEvent
        fields = ('name', 'description', 'rules', 'prizes', 'subtitle',
                  'id', 'minparticipants', 'maxparticipants')


class CompetitionsGenreSerializer(serializers.ModelSerializer):
    events = CompetitionsEventSerializer(many=True, read_only=True)

    class Meta:
        model = CompetitionsGenre
        fields = ('name', 'description', 'events', 'image')

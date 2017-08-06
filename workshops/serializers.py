from rest_framework import serializers
from .models import WorkshopsGenre, WorkshopsEvent


class WorkshopsEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkshopsEvent
        fields = ('name', 'description')


class WorkshopsGenreSerializer(serializers.ModelSerializer):
    events = WorkshopsEventSerializer(many=True, read_only=True)

    class Meta:
        model = WorkshopsGenre
        fields = ('name', 'description', 'events')

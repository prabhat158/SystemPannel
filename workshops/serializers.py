from rest_framework import serializers
from .models import WorkshopsGenre, WorkshopsEvent


class WorkshopsEventSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkshopsEvent
        fields = ('id','name', 'description', 'subtitle')


class WorkshopsGenreSerializer(serializers.ModelSerializer):
    events = WorkshopsEventSerializer(many=True, read_only=True)

    class Meta:
        model = WorkshopsGenre
        fields = ('name', 'description', 'events', 'image')

from rest_framework import serializers
from .models import CompetitionsEvent, CompetitionsGenre


class CompetitionsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionsEvent
        fields = ('name', 'LYP_description', 'LYP_img', 'LYP_logo', 'queries' , 'winners' ,'description', 'rules', 'prizes', 'subtitle','status',
                  'id', 'minparticipants', 'maxparticipants','LYP_partner')


class CompetitionsGenreSerializer(serializers.ModelSerializer):
    events = CompetitionsEventSerializer(many=True, read_only=True)

    class Meta:
        model = CompetitionsGenre
        fields = ('name', 'description', 'events', 'image')

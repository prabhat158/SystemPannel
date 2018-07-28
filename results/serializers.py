from .models import ResultsEvent
from rest_framework import serializers


class ResultsEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResultsEvent
        fields = "__all__"

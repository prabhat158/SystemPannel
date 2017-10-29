from .models import LivewireBand
from rest_framework import serializers


class LivewireBandSerializer(serializers.ModelSerializer):
    class Meta:
        model = LivewireBand
        fields = "__all__"

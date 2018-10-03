from rest_framework import serializers
from .models import rider

class RiderSerializer(serializers.ModelSerializer):
    class Meta:
        model = rider
        fields = "__all__"

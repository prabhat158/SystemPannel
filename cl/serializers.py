from .models import ContingentLeader
from rest_framework import serializers


class ContingentLeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContingentLeader
        fields = "__all__"

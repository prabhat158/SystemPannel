from .models import ContingentLeader, Contingent
from rest_framework import serializers


class ContingentLeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContingentLeader
        fields = "__all__"

class GetContingentSerializer(serializers.ModelSerializer):
    contingent_members = serializers.SlugRelatedField(
        many=True,
        slug_field='mi_number',
        read_only=True
    )
    class Meta:
        model = Contingent
        fields = ("cl", "cl_name", "cl_mobile_number", "contingent_college", "contigent_city", "contingent_strength", "strength_alloted", "status", "contingent_members")

class ContingentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contingent
        fields = "__all__"

class ApprovedSerializer(serializers.ModelSerializer):
    contingent_members = serializers.SlugRelatedField(
        many=True,
        slug_field='mi_number',
        read_only=True
    )
    class Meta:
        model = Contingent
        fields = ("contingent_members",)


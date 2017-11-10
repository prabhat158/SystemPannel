from .models import ContingentLeader, Contingent, ContingentMember
from rest_framework import serializers


class ContingentLeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContingentLeader
        fields = "__all__"

class ContingentMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContingentMember
        fields = ["profile","is_selected","is_imp","has_paid","get_name","get_mi_number","get_email","get_mobile_number"]

class GetContingentSerializer(serializers.ModelSerializer):
    contingent_members = ContingentMemberSerializer(many=True, read_only=True)
    class Meta:
        model = Contingent
        fields = ["cl","comments","contingent_members","contingent_strength","selected_contingent_strength","is_equal","strength_alloted","is_approved","get_cl_name","get_cl_college","get_cl_city"]

class ContingentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contingent
        fields = "__all__"

'''
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
'''

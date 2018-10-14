from rest_framework import serializers
from .models import UserProfile, City, College, Group, WorkshopParticipant


class UserGetSerializer(serializers.ModelSerializer):
    present_city = serializers.SlugRelatedField(
        slug_field='city_name',
        read_only=True
    )
    present_college = serializers.SlugRelatedField(
        slug_field='college_name',
        read_only=True
    )

    class Meta:
        model = UserProfile
        fields = ("name", "google_id", "mi_number", "email", "mobile_number","gender",
                  "present_city", "present_college","permanent_address",
                  "postal_address", "zip_code", "year_of_study",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    
    present_city = serializers.SlugRelatedField(
        slug_field='city_name',
        read_only=True
    )
    present_college = serializers.SlugRelatedField(
        slug_field='college_name',
        read_only=True
    )
    leader = serializers.SlugRelatedField(
        slug_field='mi_number',
        read_only=True
    )
    members = UserGetSerializer(read_only=True, many=True)

    class Meta:
        model = Group
        fields = "__all__"




class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class CollegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = College
        fields = '__all__'

class WorkshopParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkshopParticipant
        fields = '__all__'

from .models import ScheduleEvent, Check
from rest_framework import serializers


class ScheduleEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleEvent
        fields = "__all__"

class CheckSerializer(serializers.ModelSerializer):
	class Meta:
		model = Check
		fields = "__all__"

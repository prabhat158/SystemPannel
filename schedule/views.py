from .serializers import ScheduleEventSerializer, CheckSerializer
from .models import ScheduleEvent, Check
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class get_schedule_events(APIView):
    def get(self, request, format=None):
        allevents = ScheduleEvent.objects.all()
        alleventserializer = ScheduleEventSerializer(allevents,
                                                     many=True)
        return Response(alleventserializer.data)

class get_check(APIView):
    def get(self, request, format=None):
        c = Check.objects.get(pk=1)
        cserializer = CheckSerializer(c)
        return Response(cserializer.data)

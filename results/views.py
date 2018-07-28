from .serializers import ResultsEventSerializer
from .models import ResultsEvent
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class get_results_events(APIView):
    def get(self, request, format=None):
        allevents = ResultsEvent.objects.all()
        alleventserializer = ResultsEventSerializer(allevents,
                                                     many=True)
        return Response(alleventserializer.data)

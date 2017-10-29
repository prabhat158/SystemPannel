from .serializers import ContingentLeaderSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import UserProfile


class createcl(APIView):
    def post(self, request, format=None):
        info = request.data
        try:
            info['clprofile'] = UserProfile.objects.get(mi_number=info['mi_number']).id
        except:
            return Response({"details": "MI Number Invalid"},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = ContingentLeaderSerializer(data=info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import NewsSerializer
from .models import News


class NewsView(APIView):

    def get(self, request, format=None):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)

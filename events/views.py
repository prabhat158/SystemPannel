from rest_framework.views import APIView
from rest_framework.response import Response

from concerts.serializers import ConcertsGenreSerializer
from workshops.serializers import WorkshopsGenreSerializer
from proshows.serializers import ProshowsGenreSerializer
from informals.serializers import InformalsGenreSerializer
from artsandideas.serializers import ArtsAndIdeasGenreSerializer

from proshows.models import ProshowsGenre
from workshops.models import WorkshopsGenre
from concerts.models import ConcertsGenre
from informals.models import InformalsGenre
from artsandideas.models import ArtsAndIdeasGenre


class Events(APIView):
    def get(self, request, format=None):
        proshowsgenres = ProshowsGenre.objects.all()
        workshopsgenres = WorkshopsGenre.objects.all()
        concertsgenre = ConcertsGenre.objects.all()
        informalsgenres = InformalsGenre.objects.all()
        artsandideasgenres = ArtsAndIdeasGenre.objects.all()

        proshowserializer = ProshowsGenreSerializer(proshowsgenres,
                                                    many=True)
        workshopserializer = WorkshopsGenreSerializer(workshopsgenres,
                                                      many=True)
        concertserializer = ConcertsGenreSerializer(concertsgenre,
                                                    many=True)
        informalserializer = InformalsGenreSerializer(informalsgenres,
                                                      many=True)
        artsandideaserializer = ArtsAndIdeasGenreSerializer(artsandideasgenres,
                                                            many=True)

        return Response({
            "Proshows": proshowserializer.data,
            "Workshops": workshopserializer.data,
            "Pronites": concertserializer.data,
            "Informals": informalserializer.data,
            "Arts and Ideas": artsandideaserializer.data
        })

from rest_framework.views import APIView
from rest_framework.response import Response

from competitions.serializers import CompetitionsGenreSerializer
from concerts.serializers import ConcertsGenreSerializer
from workshops.serializers import WorkshopsGenreSerializer
from proshows.serializers import ProshowsGenreSerializer
from informals.serializers import InformalsGenreSerializer
from artsandideas.serializers import ArtsAndIdeasGenreSerializer

from competitions.models import CompetitionsGenre
from proshows.models import ProshowsGenre
from workshops.models import WorkshopsGenre
from concerts.models import ConcertsGenre
from informals.models import InformalsGenre
from artsandideas.models import ArtsAndIdeasGenre


class Events(APIView):
    def get(self, request, format=None):
        competitionsgenres = CompetitionsGenre.objects.all()
        proshowsgenres = ProshowsGenre.objects.all()
        workshopsgenres = WorkshopsGenre.objects.all()
        concertsgenre = ConcertsGenre.objects.all()
        informalsgenres = InformalsGenre.objects.all()
        artsandideasgenres = ArtsAndIdeasGenre.objects.all()

        competitionserializer = CompetitionsGenreSerializer(competitionsgenres,
                                                            many=True)
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
            "Competitions": competitionserializer.data,
            "Proshows": proshowserializer.data,
            "Workshops": workshopserializer.data,
            "Pronites": concertserializer.data,
            "Informals": informalserializer.data,
            "Arts and Ideas": artsandideaserializer.data
        })


class Compireg(APIView):
    def post(self, request, event_id, format=None):
        return

class UserCompetitions(APIView):
    def get(self, request, fb_id, format=None):
        return

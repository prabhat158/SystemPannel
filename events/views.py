from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from competitions.serializers import CompetitionsGenreSerializer
from concerts.serializers import ConcertsGenreSerializer
from workshops.serializers import WorkshopsGenreSerializer
from proshows.serializers import ProshowsGenreSerializer
from informals.serializers import InformalsGenreSerializer
from artsandideas.serializers import ArtsAndIdeasGenreSerializer

from competitions.serializers import CompetitionsEventSerializer
from users.serializers import GroupSerializer, WorkshopParticipantSerializer

from competitions.models import CompetitionsGenre, CompetitionsEvent
from proshows.models import ProshowsGenre, ProshowsEvent
from workshops.models import WorkshopsGenre, WorkshopsEvent
from concerts.models import ConcertsGenre
from informals.models import InformalsGenre
from artsandideas.models import ArtsAndIdeasGenre

from users.models import UserProfile, WorkshopParticipant


class Events(APIView):
    def get(self, request, format=None):
        competitionsgenres = CompetitionsGenre.objects.all()
        proshowsgenres = ProshowsGenre.objects.all()
        workshopsgenres = WorkshopsGenre.objects.all()
        concertsgenres = ConcertsGenre.objects.all()
        informalsgenres = InformalsGenre.objects.all()
        artsandideasgenres = ArtsAndIdeasGenre.objects.all()

        competitionserializer = CompetitionsGenreSerializer(competitionsgenres,
                                                            many=True)
        proshowserializer = ProshowsGenreSerializer(proshowsgenres,
                                                    many=True)
        workshopserializer = WorkshopsGenreSerializer(workshopsgenres,
                                                      many=True)
        concertserializer = ConcertsGenreSerializer(concertsgenres,
                                                    many=True)
        informalserializer = InformalsGenreSerializer(informalsgenres,
                                                      many=True)
        artsandideaserializer = ArtsAndIdeasGenreSerializer(artsandideasgenres,
                                                            many=True)

        return Response({
            "Competitions": competitionserializer.data,
            "Proshows": proshowserializer.data,
            "Workshops": workshopserializer.data,
            "Concerts": concertserializer.data,
            "Informals": informalserializer.data,
            "Arts and Ideas": artsandideaserializer.data
        })


class Compireg(APIView):
    def post(self, request, event_id, format=None):

        info = request.data
        participant = info['applicants']

        try:
            info['event'] = CompetitionsEvent.objects.get(pk=event_id).id
        except:
            return Response({"details": "Event invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            group_leader = UserProfile.objects.get(mi_number=participant[0])
        except:
            return Response({"details": "MI Number invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

        info['name'] = group_leader.mi_number
        info['mobile_number'] = group_leader.mobile_number
        info['present_city'] = group_leader.present_city.id
        info['present_college'] = group_leader.present_college.id
        info['members'] = []

        for user in participant:
            try:
                info['members'].append(UserProfile.objects.get(mi_number=user).id)
            except:
                return Response({"details": "MI Number invalid"},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = GroupSerializer(data=info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Workshopreg(APIView):
    def post(self, request, event_id, format=None):

        info = request.data
        applicant = info
        try:
            applicant['event']= ProshowsEvent.objects.get(pk=event_id).id
            '''applicant['event'] = event'''
        except:
            return Response({"details": "Event invalid"},status=status.HTTP_400_BAD_REQUEST)
        participant = WorkshopParticipantSerializer(data=applicant)
        if participant.is_valid():
            participant.save()
            return Response({"details": "Your Registration has been taken into consideration"},status=status.HTTP_201_CREATED)
        return Response({"details": "Mobile Number/Name is incorrect"},status=status.HTTP_400_BAD_REQUEST)
        '''applicant = info['applicant']

        try:
            info['event'] = WorkshopsEvent.objects.get(pk=event_id).id
        except:
            return Response({"details": "Event invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            u = UserProfile.objects.get(mi_number=applicant)
            info['participant'] = u.id
        except:
            return Response({"details": "MI Number invalid"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            w = WorkshopParticipant.objects.filter(participant=u)
            for t in w:
                if t.event.id == info['event']:
                    return Response({"details": "Exists"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            serializer = WorkshopParticipantSerializer(data=info)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer = WorkshopParticipantSerializer(data=info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''



class UserCompetitions(APIView):
    def get_object(self, google_id):
        try:
            return UserProfile.objects.get(google_id=google_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, google_id, format=None):
        user = self.get_object(google_id)
        temp = []
        for group in user.group_set.all():
            if(group.event not in temp):
                temp.append(group.event)
        serializer = CompetitionsEventSerializer(temp, many=True)
        return Response(serializer.data)

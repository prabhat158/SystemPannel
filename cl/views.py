from .serializers import ContingentLeaderSerializer, ContingentSerializer, GetContingentSerializer, ApprovedSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import UserProfile
from .models import Contingent, ContingentLeader
from django.http import Http404


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

class getcontingents(APIView):
    def get(self, request, format=None):
        contingentslist = Contingent.objects.all()
        contingentserializer = GetContingentSerializer(contingentslist,
                                                    many=True)
        return Response(contingentserializer.data)
        
class createandeditcontingent(APIView):
    def get_object(self, fb_id):
        try:
            return UserProfile.objects.get(fb_id=fb_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get_cl(self, foreignkey):
        try:
            cl = ContingentLeader.objects.filter(clprofile=foreignkey)
            return cl[0]
        except ContingentLeader.DoesNotExist:
            raise Http404

    def get_contingent(self, cl):
        try:
            return Contingent.objects.get(cl=cl)
        except Contingent.DoesNotExist:
            raise Http404

    def get(self, request, fb_id, format=None):
        user = self.get_object(fb_id)
        clprofile = self.get_cl(user.pk)
        contingent = self.get_contingent(clprofile.pk)
        contingentserializer = GetContingentSerializer(contingent)
        return Response(contingentserializer.data)
    
    def post(self, request, fb_id, format=None):
        user = self.get_object(fb_id)
        cl = self.get_cl(user.pk)
        info = request.data
        print(info)
        members = info["members"]
        info['contingent_members'] = []

        for user in members:
            try:
                info['contingent_members'].append(UserProfile.objects.get(mi_number=user).id)
            except:
                return Response({"details": "MI Number invalid"},
                                status=status.HTTP_400_BAD_REQUEST)

        clprofile = cl.clprofile
        info['cl'] = cl.pk
        info['cl_name'] = clprofile.name
        info['cl_mobile_number'] = clprofile.mobile_number
        info['contingent_college'] = clprofile.present_college.id
        info['contingent_city'] = clprofile.present_city.id
        info['contingent_strength'] = len(members)+1
        info['strength_alloted'] = -1
        info['status'] = 1

        serializer = ContingentSerializer(data=info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, fb_id, format=None):
        user = self.get_object(fb_id)
        cl = self.get_cl(user.pk)
        contingent = self.get_contingent(cl.pk)


        info = request.data
        members = info["members"]
        info['contingent_members'] = []

        for user in members:
            try:
                info['contingent_members'].append(UserProfile.objects.get(mi_number=user).id)
            except:
                return Response({"details": "MI Number invalid"},
                                status=status.HTTP_400_BAD_REQUEST)

        clprofile = cl.clprofile
        info['cl'] = cl.pk
        info['cl_name'] = clprofile.name
        info['cl_mobile_number'] = clprofile.mobile_number
        info['contingent_college'] = clprofile.present_college.id
        info['contingent_city'] = clprofile.present_city.id
        info['contingent_strength'] = len(members)+1
        info['strength_alloted'] = -1
        info['status'] = 1

        serializer = ContingentSerializer(contingent,data=info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class approvedminumbers(APIView):
    def get(self, request, format=None):
        contingents = Contingent.objects.filter(status=3)
        #serializer = ApprovedSerializer(contingents, many=True)
        info = {}
        info['mi_numbers']=[]
        for contingent in contingents:
            for member in contingent.contingent_members.all():
                info['mi_numbers'].append(member.mi_number)
        return Response(info)

class checkcr(APIView):
    def post(self, request, format=None):
        info = request.data
        try:
            user = UserProfile.objects.get(mi_number=info['username'])
        except UserProfile.DoesNotExist:
            raise Http404
        try:
            cl = ContingentLeader.objects.filter(clprofile=user.pk)
        except ContingentLeader.DoesNotExist:
            raise Http404
        if(info['password']==user.fb_id):
            serializer = ContingentLeaderSerializer(cl[0])
            return Response(serializer.data)
        raise Http404

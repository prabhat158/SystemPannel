from .serializers import ContingentLeaderSerializer, GetContingentSerializer, ContingentSerializer#, ContingentSerializer, GetContingentSerializer, ApprovedSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import UserProfile
from .models import ContingentLeader, Contingent, ContingentMember#,Contingent
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

class createcl(APIView):
    def post(self, request, format=None):
        info = request.data
        #try:
            #info['clprofile'] = UserProfile.objects.get(mi_number=info['mi_number'])
        #except UserProfile.DoesNotExist:
            #return Response({"details": "MI Number Invalid"},
                            #status=status.HTTP_400_BAD_REQUEST)
        cl= get_object_or_404(UserProfile.objects, mi_number=info['mi_number'])
        
        inf={
                'clprofile':cl.id,
                'college':info['college'],
                'por':info['por'],
                'wascllastyear':info['wascllastyear'],
                'iscrcurrently':info['iscrcurrently'],
                'timesmiattended':info['timesmiattended'],
                'nocpiclink':info['nocpiclink'],
                'year_of_study':info['year_of_study'],
                'city':info['city']
                }
        serializer = ContingentLeaderSerializer(data=inf)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class checkcl(APIView):
    def post(self, request, format=None):
        info = request.data
        try:
            user = UserProfile.objects.get(mi_number=info['username'])
        except UserProfile.DoesNotExist:
            return JsonResponse({'error':'User does not exist'})
        except KeyError:
            raise Http404
        try:
            cl = ContingentLeader.objects.get(cl=user.id)
        except Contingent.DoesNotExist:
            return JsonResponse({'error':user.id})
        try:
            if(info['password']==user.google_id):
                serializer = GetContingentSerializer(cl)
                return Response(serializer.data)
            else:
                return JsonResponse({'error':'Password is wrong'})
        except KeyError:
            raise Http404

class createandeditcontingent(APIView):
    def get_object(self, fb_id):
        try:
            return UserProfile.objects.get(fb_id=fb_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get_contingent(self, cl):
        try:
            return Contingent.objects.get(cl=cl)
        except Contingent.DoesNotExist:
            raise Http404

    def get_or_create_member(self, userprofile):
        try:
            print('exists')
            return ContingentMember.objects.get(profile=userprofile).id
        except ContingentMember.DoesNotExist:
            print('creating')
            return ContingentMember.objects.create(profile=userprofile).id
    
    def post(self, request, fb_id, format=None):
        user = self.get_object(fb_id)
        contingent = self.get_contingent(user.pk)
        info = {}
        info["members"] = request.data["members"]
        print(info)
        members = info["members"]
        info['contingent_members'] = []

        for member in members:
            try:
                temp = UserProfile.objects.get(mi_number=member)
                memberid=self.get_or_create_member(temp)
                info['contingent_members'].append(memberid)
            except:
                return Response({"details": "MI Number invalid"},
                                status=status.HTTP_400_BAD_REQUEST)

        info['cl'] = user.id
        info['contingent_strength'] = len(members)

        serializer = ContingentSerializer(contingent,data=info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class selectmembers(APIView):
    def get_object(self, fb_id):
        try:
            return UserProfile.objects.get(fb_id=fb_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get_contingent(self, cl):
        try:
            return Contingent.objects.get(cl=cl)
        except Contingent.DoesNotExist:
            raise Http404

    def get_member(self, userprofile):
        try:
            print('exists')
            return ContingentMember.objects.get(profile=userprofile)
        except ContingentMember.DoesNotExist:
            print('creating')
            raise Http404
    
    def post(self, request, fb_id, format=None):
        user = self.get_object(fb_id)
        contingent = self.get_contingent(user.pk)
        members = request.data["members"]
        actualmembers = contingent.contingent_members.all()
        print(actualmembers)
        for member in actualmembers:
            if member.get_mi_number() in members:
                member.is_selected = 1
                member.save()
            else:
                member.is_selected = 0
                member.save()
        contingent.selected_contingent_strength = len(members)
        if(contingent.selected_contingent_strength == contingent.strength_alloted):
            contingent.is_equal = 1
        else:
            contingent.is_equal = 0
        contingent.save()
        return Response({"details": "Success"},
                        status=status.HTTP_200_OK)


class approvedminumbers(APIView):
    def get_object(self, fb_id):
        try:
            return UserProfile.objects.get(mi_number=fb_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get_member(self, userprofile):
        try:
            print('exists')
            return ContingentMember.objects.get(profile=userprofile)
        except ContingentMember.DoesNotExist:
            raise Http404

    def get(self, request, mi_number, format=None):
        user = self.get_object(mi_number)
        member = self.get_member(user)
        if member.is_selected==1:
            return Response({"detail":True})
        else:
            return Response({"detail":False})

class updatepaidlist(APIView):
    def get_object(self, fb_id):
        try:
            return UserProfile.objects.get(mi_number=fb_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get_member(self, userprofile):
        try:
            print('exists')
            return ContingentMember.objects.get(profile=userprofile)
        except ContingentMember.DoesNotExist:
            raise Http404

    def post(self, request, format=None):
        info = request.data
        print(info)
        if(isinstance(info, list)):
            print("list")
            for instance in info:
                mi_number = instance["answerList"][0]["answer"]
                user = self.get_object(mi_number)
                member = self.get_member(user)
                member.has_paid = 1
                member.save()
            return Response({"detail":"Success"})
        else:
            print("single")
            mi_number = info["answerList"][0]["answer"]
            user = self.get_object(mi_number)
            member = self.get_member(user)
            member.has_paid = 1
            member.save()
            return Response({"detail":"Success"})
        '''
        contingents = Contingent.objects.filter(status=3)
        
        #serializer = ApprovedSerializer(contingents, many=True)
        info = {}
        info['mi_numbers']=[]
        for contingent in contingents:
            for member in contingent.contingent_members.all():
                info['mi_numbers'].append(member.mi_number)
        '''

'''
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
'''
'''
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
'''

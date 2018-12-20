from .serializers import VisitSerializer, ContingentLeaderSerializer, GetContingentSerializer, ContingentSerializer, CollegeSerializer, ContingentMemberSerializer#, ContingentSerializer, GetContingentSerializer, ApprovedSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import UserProfile
from users.serializers import UserSerializer
from .models import Visits, ContingentLeader, Contingent, ContingentMember, College#,Contingent
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404

class colleges(APIView):

    def get(self,request, pin_code, *args, **kwargs):
        #colleges = College.objects.all().order_by('name')
        colleges = College.objects.filter(pin_code=pin_code)
        serializer = CollegeSerializer(colleges, many=True)
        return Response(serializer.data)

class visit(APIView):
    def delete_extra(self, user):
        if Visits.objects.filter(visitor=user):
            inst = Visits.objects.filter(visitor=user).first()
            inst.delete()
        return

    def post(self, request, google_id):
        info=request.data
        inf={}
        inf["pin_code"]=info["pin_code"]
        inf["visitor"]= get_object_or_404(UserProfile.objects, google_id=google_id).id
        inf["gender"] = info["gender"]
        '''if(Visits.objects.get(visitor=inf["visitor"])
            Visits.objects.filter(visitor__mi_number=inf["visitor"].mi_number)[0].delete()'''
        self.delete_extra(inf["visitor"])
        
        serializer= VisitSerializer(data=inf)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, google_id, *args, **kwargs):
        visitor = get_object_or_404(UserProfile.objects, google_id=google_id).id 
        visit = get_object_or_404(Visits.objects, visitor=visitor)
        serializer = VisitSerializer(visit)
        return Response(serializer.data)
        '''if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''

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
            cl = Contingent.objects.get(cl=user.id)
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

class createmember(APIView):
    def get_or_add_member(self, user, college, gender, cont):
        try:
            member = ContingentMember.objects.get(profile=user)
            member.contingent_set.clear()
            member.gender = gender
            member.college = college
            member.save()
            cont.contingent_members.add(member)
            cont.save()
            return member
        except ContingentMember.DoesNotExist:
            member = ContingentMember.objects.create(profile=user, gender=gender, college=college)
            cont.contingent_members.add(member)
            cont.contingent_strength += 1
            if(gender=="Male"):
                cont.m_strength += 1
            else:
                cont.f_strength += 1
            cont.save()
            return member

    def post(self, request, google_id):
        info=request.data
        user = get_object_or_404(UserProfile.objects, google_id=google_id)
        college = get_object_or_404(College.objects, name=info["college"])
        contingent = get_object_or_404(Contingent.objects, college=college)
        new_member = self.get_or_add_member(user, college, info["gender"], contingent)
        
        
        serializer = ContingentMemberSerializer(new_member)
        return Response(serializer.data)

    def get(self, request, google_id):
        user = get_object_or_404(UserProfile.objects, google_id=google_id)
        member = get_object_or_404(ContingentMember.objects, profile=user)
        serializer = ContingentMemberSerializer(member)
        return Response(serializer.data)

class getcl(APIView):
    def get(self, request, google_id):
        user = get_object_or_404(UserProfile.objects, google_id=google_id)
        member = get_object_or_404(ContingentMember.objects, profile=user)
        college = member.college
        contingent = get_object_or_404(Contingent.objects, college=college)
        #leader = get_object_or_404(UserProfile.objects, pk=contingent.cl)
        leader = contingent.cl
        serializer=UserSerializer(leader)
        return Response(serializer.data)
class getcl_college(APIView):
    def post(self, request):
        info = request.data
        college = get_object_or_404(College.objects, name=info["college"])
        contingent = get_object_or_404(Contingent.objects, college=college)
        leader = contingent.cl
        serializer=UserSerializer(leader)
        return Response(serializer.data)
class getcollege(APIView):
    def get(self, request, google_id):
        user = get_object_or_404(UserProfile.objects, google_id=google_id)
        member = get_object_or_404(ContingentMember.objects, profile=user)
        college = member.college
        serializer = CollegeSerializer(college)
        return Response(serializer.data)

class createandeditcontingent(APIView):
    def get_object(self, google_id):
        try:
            return UserProfile.objects.get(google_id=google_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get_contingent(self, cl):
        try:
            return Contingent.objects.get(cl=cl)
        except Contingent.DoesNotExist:
            raise Http404

    def get_or_create_member(self, userprofile, gender, cl_approve, college):
        try:
            print('exists')
            member=ContingentMember.objects.get(profile=userprofile)
            member.gender = gender
            member.cl_approve = cl_approve
            member.college = college
            member.save()
            return member.id
        except ContingentMember.DoesNotExist:
            print('creating')
            try:
                return ContingentMember.objects.create(profile=userprofile, gender=gender, cl_approve=0, college=college).id
            except KeyError:
                return ContingentMember.objects.create(profile=userprofile, gender=gender, cl_approve=0, college=college).id

    def post(self, request, google_id, format=None):
        user = self.get_object(google_id)
        contingent = self.get_contingent(user.pk)
        info = {}
        info["members"] = request.data["members"]
        print(info)
        members = info["members"]
        info['contingent_members'] = []
        info['m_strength'] = 0
        info['f_strength'] = 0

        for member in members:
            '''try:
                temp = UserProfile.objects.get(mi_number=member)
                print(here1)
                memberid=self.get_or_create_member(temp)
                print(here2)
                info['contingent_members'].append(memberid)
            except:
                return Response({"details": "MI Number invali1d"},
                                status=status.HTTP_400_BAD_REQUEST)'''
            temp = get_object_or_404(UserProfile.objects, mi_number=member["mi_number"])
            '''try:
                memberid = self.get_or_create_member(temp)
            except:
                return Response({"details": "MI Number invali1d"},
                                status=status.HTTP_400_BAD_REQUEST)'''
            memberid = self.get_or_create_member(temp, member["gender"], member["cl_approve"], contingent.college)
            if(member["gender"]=="Male"):
                info['m_strength'] += 1
            else:
                info['f_strength'] += 1
            info['contingent_members'].append(memberid)

        info['cl'] = user.id
        info['contingent_strength'] = len(members)

        serializer = ContingentSerializer(contingent,data=info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class selectmembers(APIView):
    def get_object(self, google_id):
        try:
            return UserProfile.objects.get(google_id=google_id)
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
    
    def post(self, request, google_id, format=None):
        user = self.get_object(google_id)
        contingent = self.get_contingent(user.pk)
        members = request.data["members"]
        actualmembers = contingent.contingent_members.all()
        #print(actualmembers)
        contingent.selected_m=0
        contingent.selected_f=0
        for member in actualmembers:
            if member.get_mi_number() in members:
                member.is_selected = 1
                if(member.gender=="Male"):
                    contingent.selected_m +=1
                if(member.gender=="Female"):
                    contingent.selected_f +=1
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
    def get_object(self, google_id):
        try:
            return UserProfile.objects.get(mi_number=google_id)
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

class approvedcl(APIView):
    def get(self, request, mi_number, format=None):
        try:
            cont = Contingent.objects.filter(cl__mi_number=mi_number)[0]
            return Response({"detail":True})
        except:
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

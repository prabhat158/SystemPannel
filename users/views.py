from .models import UserProfile, City, College
from .serializers import UserGetSerializer, UserSerializer
from .serializers import CitySerializer, CollegeSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import unidecode


class cities(APIView):

    def get(self, request, format=None):
        print("hi")
        cities = City.objects.all().order_by('city_name')
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)


class colleges(APIView):
    def get_object(self, city_id):
        try:
            return City.objects.get(pk=city_id).college_set.all().order_by('college_name')
        except City.DoesNotExist:
            raise Http404

    def get(self, request, city_id, format=None):
        colleges = self.get_object(city_id=city_id)
        serializer = CollegeSerializer(colleges, many=True)
        return Response(serializer.data)


class getuser(APIView):
    def get_object(self, fb_id):
        try:
            return UserProfile.objects.get(fb_id=fb_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, fb_id, format=None):
        user = self.get_object(fb_id)
        serializer = UserGetSerializer(user)
        return Response(serializer.data)


def giveFirstThree(word):
    word = word[:3]
    word = unidecode.unidecode(word)
    word = word.replace(" ", "")
    ans = ""
    for letter in word:
        temp = ord(letter)
        if temp <= ord('z') and temp >= ord('a'):
            ans += chr(temp + ord('A') - ord('a'))
        else:
            ans += letter
    return ans


class createuser(APIView):
    def post(self, request, format=None):
        info = request.data
        try:
            info['present_city'] = City.objects.filter(city_name=info['present_city'])[0].id
            print("city exists")
        except:
            info['present_city'] = City.objects.create(city_name=info['present_city']).id
            print("new city")
        try:
            info['present_college'] = College.objects.filter(college_name=info['present_college'], located_city=int(info['present_city']))[0].id
            print("college exists")
        except:
            Cityinstance = City.objects.filter(id=info['present_city'])[0]
            info['present_college'] = College.objects.create(college_name=info['present_college'], located_city=Cityinstance).id
            print("new college")

        name = info['name']
        beg = giveFirstThree(name)
        beg = "MI-" + beg + "-"
        already_there = len(UserProfile.objects.filter(mi_number__startswith=beg))
        if already_there == 0:
            end = "101"
        else:
            end = str(101 + already_there)
        info['mi_number'] = beg + end

        print(info)

        serializer = UserSerializer(data=info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        '''
        try:
            new_user = UserProfile.objects.create(name=request.data['name'], postal_address=request.data['postal_address'], mobile_number=request.data['mobile_number'], whatsapp_number=request.data['whatsapp_number'], zip_code=request.data['zip_code'], year_of_study=request.data['year_of_study'], fb_id=request.data['fb_id'], email=request.data['email'], present_city=city, present_college=college, mi_number=(beg+"-"+end))
            print new_user
            return Response({"details":"Successful!"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"details":"Invalid"}, status = status.HTTP_400_BAD_REQUEST)
        '''

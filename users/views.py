from .models import UserProfile, City, College, Group
from .serializers import UserGetSerializer, UserSerializer
from .serializers import CitySerializer, CollegeSerializer, GroupSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from competitions.models import CompetitionsEvent
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import unidecode
import requests, json


class cities(APIView):

    def get(self, request, format=None):
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
    def get_object(self, google_id):
        try:
            return UserProfile.objects.get(google_id=google_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, google_id, format=None):
        user = self.get_object(google_id)
        serializer = UserGetSerializer(user)
        return Response(serializer.data)


class check(APIView):
    def get_object(self, google_id):
        try:
            return UserProfile.objects.get(google_id=google_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, google_id, format=None):
        user = self.get_object(google_id)
        user.checkedin = 1
        user.save()
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
            info['present_city'] = City.objects.filter(city_name=info.get('present_city'))[0].id
        except:
            city = City.objects.create(city_name=info.get('present_city'))
            info['present_city'] = city.id
        try:
            info['present_college'] = College.objects.filter(college_name=info.get('present_college'), located_city=int(info['present_city']))[0].id
        except:
            Cityinstance = City.objects.filter(id=info['present_city'])[0]
            info['present_college'] = College.objects.create(college_name=info.get('present_college'), located_city=Cityinstance).id

        name = info.get('name')
        beg = giveFirstThree(name)
        beg = "MI-" + beg + "-"
        already_there = len(UserProfile.objects.filter(mi_number__startswith=beg).order_by('-mi_number'))
        if already_there == 0:
            end = "101"
        else:
            temp = UserProfile.objects.filter(mi_number__startswith=beg)
            sortedtemp = sorted(temp, key=lambda UserProfile: int(UserProfile.mi_number[7:]))
            sortedtemp.reverse()
            end = str(int(sortedtemp[0].mi_number[7:]) + 1)
        info['mi_number'] = beg + end
        #increase CR's score if any
        #URL = "https://api.moodi.org/my_cr/"
        #data = {'referral_code':info['cr_referral_code']}
        #r = requests.post(URL, data=data)
        #print(r.json())

        serializer = UserSerializer(data=info)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        '''
        try:
            new_user = UserProfile.objects.create(name=request.data['name'], postal_address=request.data['postal_address'], mobile_number=request.data['mobile_number'], whatsapp_number=request.data['whatsapp_number'], zip_code=request.data['zip_code'], year_of_study=request.data['year_of_study'], google_id=request.data['google_id'], email=request.data['email'], present_city=city, present_college=college, mi_number=(beg+"-"+end))
            print new_user
            return Response({"details":"Successful!"}, status=status.HTTP_201_CREATED)
        except:
            return Response({"details":"Invalid"}, status = status.HTTP_400_BAD_REQUEST)
        '''
class aid(APIView):

    def getimage(self,query):
        url = 'https://api.cognitive.microsoft.com/bing/v7.0/images/search'
        headers = {
            'Ocp-Apim-Subscription-Key': '60fc159801924ff89e38e80ebd688e26'
        }
        try:
            response = requests.get(url+"?q=" + query+"&count=1", headers=headers)
            data = response.json()
            if data['value']:
                content_url =  data['value'][0]['contentUrl']
                print(content_url)
                return content_url
        except Exception as e:
            pass

    def post(self, request, format=None):

        data_string = request.data['textcontent']
        data = [s.strip() for s in data_string.splitlines()]
        print(data)

        my_list = []

        for i in range(0,min(len(data),100)):
            send_data = data[i]
            url = 'https://southeastasia.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
            payload = {
                # Request parameters
                "documents": [
                {
                  "id": "string",
                  "text": send_data   
                }
              ]
            }
            headers = {
                'Content-Type': 'application/json',
                'Ocp-Apim-Subscription-Key': 'd80ae700fdba4e839e7b209bb82ec100',
            }
            try:
                response = requests.post(url, data=json.dumps(payload), headers=headers)
                keyPhrases = response.json()
                if keyPhrases['documents']:
                    print(keyPhrases)
                    my_list.append(self.getimage(keyPhrases['documents'][0]['keyPhrases'][0]))
                    print(my_list)
            except Exception as e:
                print(e)
                return Response({"Error":e}, status= status.HTTP_400_BAD_REQUEST)
            
        return Response(my_list)


class my_team(APIView):
    
    def get(self, request, google_id, format=None):
        info = request.GET

        # Get the profile of the user if exists
        user = get_object_or_404(UserProfile.objects, google_id=google_id)

        # Get all groups if event is not specified
        if "event" not in info or not info["event"]:
            return Response(GroupSerializer(Group.objects.filter(members__mi_number=user.mi_number), many=True).data)

        # Get particular group when event is specified
        team = get_object_or_404(Group.objects, members__mi_number=user.mi_number, event__id=info["event"])
        serializer = GroupSerializer(team)
        return Response(serializer.data)


class add_member(APIView):
    """docstring for createteam"""
    def post(self, request, google_id):
        info = request.data

        # Get user object
        user = get_object_or_404(UserProfile.objects, google_id=google_id)

        # checking if the request is made by a leader
        team = get_object_or_404(Group.objects, leader__mi_number=user.mi_number, event__id=info["event_id"])

        # checking if the member exist in any other team or is a leader in other group
        member_present = Group.objects.filter(members__mi_number=info['member_number']).filter(event__id=info["event_id"]).exists()
        leader_present = Group.objects.filter(leader__mi_number=info['member_number']).filter(event__id=info["event_id"]).exists()

        # Add a new member if all is okay
        if not member_present and not leader_present:
            new_member = get_object_or_404(UserProfile.objects, mi_number=info["member_number"])
            team.members.add(new_member)
            team.save()
            serializer = GroupSerializer(team)
            return Response(serializer.data)
        raise Http404

class is_leader(APIView):
    def get(self, request, google_id, format=None):
        info = request.GET
        return Response({
            "response": Group.objects.filter(
                event__id=info["event"],
                leader__google_id=google_id
            ).exists()})
        
class exit_team(APIView):

    def post(self, request, google_id):
        info = request.data

        # finding out if the member belongs to a team
        user = get_object_or_404(UserProfile.objects, mi_number=info["mi_number"])
        team = get_object_or_404(Group.objects, members__mi_number=info["mi_number"], event__id=info["event_id"])

        # User can remove if leader OR self
        if team.leader.google_id == google_id or user.google_id == google_id:
            # Remove the member from the team
            team.members.remove(user)
            team.save()
            serializer = GroupSerializer(team)
            return Response(serializer.data)
        else:
            return Response({"detail": "forbidden"}, status=403)

class create_team(APIView):
    def post(self, request, google_id):
        info = request.data
        user = info["user"]
        try:
            leader = UserProfile.objects.filter(google_id=google_id)
            event = CompetitionsEvent.objects.filter(name=info["event_name"])
            my_team = Group.objects.create(name=info["team"]["name"], mobile_number=user["mobile_number"], event=event,
                present_city=user["present_city"], present_college=user["present_college"],
                leader=leader)

            Team = GroupSerializer(my_team)
            return Team
        except UserProfile.DoesNotExist:
            raise Http404    

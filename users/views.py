from .models import UserProfile, City, College, Group
from .serializers import UserGetSerializer, UserSerializer
from .serializers import CitySerializer, CollegeSerializer, GroupSerializer
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
    def get_object(self, fb_id):
        try:
            return UserProfile.objects.get(fb_id=fb_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, fb_id, format=None):
        user = self.get_object(fb_id)
        serializer = UserGetSerializer(user)
        return Response(serializer.data)


class check(APIView):
    def get_object(self, fb_id):
        try:
            return UserProfile.objects.get(fb_id=fb_id)
        except UserProfile.DoesNotExist:
            raise Http404

    def get(self, request, fb_id, format=None):
        user = self.get_object(fb_id)
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
            info['present_city'] = City.objects.filter(city_name=info['present_city'])[0].id
        except:
            info['present_city'] = City.objects.create(city_name=info['present_city']).id
        try:
            info['present_college'] = College.objects.filter(college_name=info['present_college'], located_city=int(info['present_city']))[0].id
        except:
            Cityinstance = City.objects.filter(id=info['present_city'])[0]
            info['present_college'] = College.objects.create(college_name=info['present_college'], located_city=Cityinstance).id

        name = info['name']
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
        URL = "https://api.moodi.org/my_cr/"
        data = {'referral_code':info['cr_referral_code']}
        r = requests.post(URL, data=data)
        print(r.json())

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
    info = request.data
    def get(self, request, fb_id, format=None):
        try:
            User = UserProfile.objects.filter(fb_id=fb_id)
            try:
                team = Group.objects.filter(members__mi_number=User.mi_number, event_name=info["event_name"])
                return team
            except Group.DoesNotExist:
                raise Http404
        except User.DoesNotExist
            raise Http404


class add_member(APIView):
    """docstring for createteam"""
    def post(self, request, fb_id):
        info = request.data
        try:
            User = UserProfile.objects.filter(fb_id=fb_id)
            try:
                #checking if the request is made by a leader
                team = Group.objects.filter(leader_mi_number=User.mi_number, event_name=info["compi_name"])
                try:
                    #checking if the member exist in any other team or is a leader in other group
                    if !(Group.objects.filter(members__mi_number=info['member_number'], event_name=info["compi_name"]).count()+Group.objects.filter(leader_mi_number=info['member_number'], event_name=info["compi_name"]).count())
                        New_member=UserProfile.objects.filter(mi_number=info['member_number'])
                        team.memebers.add(New_member)
                        Team
                        return team
                    raise Http404
                except UserProfile.DoesNotExist:
                    raise Http404
            except Group.DoesNotExist:
                raise Http404
        except UserProfile.DoesNotExist:
            raise Http404

class is_leader(APIView):
    def get(self, request, fb_id, format=None):
        info = request.data
        try:
            Team = Group.objects.filter(event_name=info["event_name"], leader_mi_number=info["mi_number"])
            return True
        except Group.DoesNotExist:
            return False
        
class exit_team(APIView):

    def post(self, request):
        info = request.data
        try:
            #finding out if the member belongs to a team
            team = Group.objects.filter(memebers__mi_number=info["mi_number"], event_name=info["compi_name"])
            User = UserProfile.objects.filter(mi_number=info["mi_number"])
            team.members.remove(User)
        except Group.DoesNotExist:
            raise Http404


class create_team(APIView):
    def post(self, request, fb_id):
        info = request.data
        user = info['user']
        try:
            leader = UserProfile.objects.filter(fb_id=fb_id)
            event = CompetitionsEvent.objects.filter(name=info['event_name'])
            my_team = Group.objects.create(name=info['team']['name'], mobile_number=user['mobile_number'], event=event,
                present_city=user['present_city'], present_college=user['present_college'],
                leader=leader)

            Team = GroupSerializer(my_team)
            return Team
        except UserProfile.DoesNotExist:
            raise Http404    

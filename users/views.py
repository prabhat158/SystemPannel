from .models import UserProfile, City, College, Group
from .serializers import UserGetSerializer, UserSerializer
from .serializers import CitySerializer, CollegeSerializer, GroupSerializer
from django.shortcuts import get_list_or_404, get_object_or_404
from competitions.models import CompetitionsEvent, MuticityCompetitionsEvent
from django.http import Http404, JsonResponse
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import unidecode
from django.template import loader
import requests, json
from rest_framework.decorators import api_view


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
        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['POST',])
def get_mino(request, mi_no, format=None):
    if 'secret' in request.data and request.data['secret'] == 'mimi123':
        user = get_object_or_404(UserProfile.objects, mi_number=mi_no)
        return Response(UserSerializer(user).data)
    return Response(status=403)
class get_user(APIView):
    def post(self, request): 
        mi_num = request.data['mi_number']
        user = get_object_or_404(UserProfile.objects, mi_number=mi_num)
        serializer = UserSerializer(user)
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
        serializer = UserSerializer(user)
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
        URL = "https://api.moodi.org/my_cr/"
        data = {'referral_code':info['cr_referral_code'], 'score':'10'}
        r = requests.post(URL, data=data)
        #print(r.json())

        serializer = UserSerializer(data=info)
        if serializer.is_valid():
            serializer.save()
            if info['status'] == 'multicity':
                send_mail('Welcome to Mood Indigo Multicity Eliminations 2019',
                '',
                'Mood Indigo <publicrelations@moodi.org>', [info['email']], fail_silently=True, html_message='''<!DOCTYPE html>

                <html>
                <head></head>
                <body>
                <p>Hi ''' + info['name'] + '''
                <p><b>Greetings from Mood Indigo!</b></p>
                <p>Welcome to the Multicity Eliminations of Asia's largest college cultural festival!<br/>
                This year, we are reaching out to more than 10 cities to pick the best of the best to showcase their talent at Mood Indigo:</p>
                <ul>
                <li><b>Bangalore -</b> September 1, 2019</li>
                <li><b>Kolkata -</b> September 8, 2019</li>
                <li><b>Bhopal -</b> September 26, 2019 - September 29, 2019</li>
                <li><b>Pune -</b> September 29, 2019</li>
                <li><b>Nagpur -</b> October 5, 2019 - October 6, 2019; Fest Dates- October 18, 2019 - October 20, 2019</li>
                <li><b>Delhi -</b> October 12, 2019 - October 13, 2019</li>
                <li><b>Jaipur -</b> October 18, 2019 - October 20, 2019</li>
                <li><b>Bhubaneswar -</b> November 8, 2019 - November 10, 2019</li>
                <li><b>Chandigarh -</b> November 8, 2019 - November 10, 2019</li>
                <li><b>Mumbai -</b> December 1, 2019</li>
                </ul>
                <p>Now that you've registered as a participant of the eliminations, time to go to your city's tab at <a href="https://multicity.moodi.org/">multicity.moodi.org</a> and register for the competitions you want to participate in.<br/>
                Register at <a href="https://ccp.moodi.org"><b>College Connect Program</b></a> to join Mood Indigo's organising team!
                </p><br\>
                Do follow us on <a href="https://www.facebook.com/iitb.moodindigo/">Facebook</a>, <a href="https://www.instagram.com/iitbombay.moodi/">Instagram</a> and <a href="https://twitter.com/iitb_moodi">Twitter</a> for regular updates regarding the eliminations including venues and rules of competitions!<br>All the best for your journey at Mood Indigo! 
                

                </body>
                </html>

                ''')
            else:
                send_mail('Congratulations! Registration for Mood Indigo 2k18 successful!',
                    '',
                    'Mood Indigo <publicrelations@moodi.org>', [info['email']], fail_silently=True, html_message='''<!DOCTYPE html>

                    <html>
                    <head></head>
                    <body>
                    <p>Greetings from Mood Indigo!</p>

                    <p>Congratulations on successfully registering for <b>Mood Indigo 2k18!</b><br/>
                    Come to the City of Dreams this December and witness the most amazing performances from all across the world. A plethora of events awaits you where you will never be able to see it all. But what you see, will last a lifetime!</p>

                    <p>Join us for the 48th edition of Mood Indigo from <b>27th December - 30th December!</b></p>

                    <p><b>Your registration number is ''' + info['mi_number'] + ''' </b></p>

                    <p>Looking forward to having you here at Mood Indigo!</p>

                    <p>For any queries, visit our website - <a href="https://moodi.org">https://moodi.org</a><br/>
                    For updates, follow us on <a href="https://www.facebook.com/iitb.moodindigo/">Facebook</a>, <a href="https://www.instagram.com/iitbombay.moodi/">Instagram</a> and <a href="https://twitter.com/iitb_moodi">Twitter</a>.
                    </p>

                    </body>
                    </html>

                    '''
                )

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


class leader_name(APIView):
    def get(self, request, mi_number):
        user=get_object_or_404(UserProfile.objects, mi_number=mi_number)
        data={'leader_name':user.name}
        return JsonResponse(data)

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
        member_present = Group.objects.filter(members__mobile_number=info['member_number']).filter(event__id=info["event_id"]).exists()
        leader_present = Group.objects.filter(leader__mobile_number=info['member_number']).filter(event__id=info["event_id"]).exists()

        # Add a new member if all is okay
        if not member_present and not leader_present:
            new_member = get_object_or_404(UserProfile.objects, mobile_number=info["member_number"])
            team.members.add(new_member)
            team.save()
            serializer = GroupSerializer(team)
            return Response(serializer.data)
        raise Http404

class is_leader(APIView):
    def get(self, request, google_id, format=None):
        info = request.GET
        team = get_object_or_404(Group.objects, leader__google_id=google_id, event__id=info["event"])
        serializer = GroupSerializer(team)
        return Response(serializer.data)
        
class exit_team(APIView):

    def post(self, request, google_id):
        info = request.data

        # finding out if the member belongs to a team
        user = get_object_or_404(UserProfile.objects, mobile_number=info["number"])
        team = get_object_or_404(Group.objects, members__mobile_number=info["number"], event__id=info["event_id"])

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

        # Get objects
        leader = get_object_or_404(UserProfile.objects, google_id=google_id)
        event  = get_object_or_404(MuticityCompetitionsEvent.objects, id=info["event_id"])

        # Check if already present in a team
        if Group.objects.filter(members__mi_number=leader.mi_number, event=event).exists():
            return Response({"detail": "User already present in another group"}, status=403)

        # Check if leading another team
        if Group.objects.filter(leader=leader, event=event).exists():
            return Response({"detail": "User already leads another group"}, status=403)

        # Create a team
        my_team = Group.objects.create(
                name=leader.name,
                mobile_number=leader.mobile_number,
                event=event,
                present_city=leader.present_city,
                present_college=leader.present_college,
                leader=leader,
                multicity=info["multicity"])
        return Response(GroupSerializer(my_team).data)


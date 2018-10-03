from django.shortcuts import render
from django.http import Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RiderSerializer

class book_ticket(APIView):
    def post(self, request):
        regs = request.data
        serializer = RiderSerializer(data = info)
        for reg in regs:
            info={}
            info['name'] = reg['userName']
            info['email'] = reg['userEmailId']
            info['ticketName'] = reg['ticketName']
            info['ticketPrice'] = reg['ticketPrice']
            for answer in reg.answerList:
                ques = answer["question"].lower()
                if ques=="college name":
                    info['college'] = answer["answer"]
                elif ques[0]=="c":
                    info[cr_refferal_code]= answer["answer"]
                elif ques[0]=="b":
                    info["bus_pickup"] = answer["answer"]
                elif ques[0]=="p":
                    info["mobile_number"] = answer["answer"]
            serializer = RiderSerializer(data = info)
            if serializer.is_valid():
                serializer.save()
            else:
                raise Http404
        return Response(serializer.data)
        

# Create your views here.

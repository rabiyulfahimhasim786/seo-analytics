from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect

from django.http import HttpResponse
import json
from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response
from .serializers import ChatSerializer

from .models import Chat

from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import serializers
import openai

# Create your views here.
def chatgptindex(request):
    return HttpResponse("Hello, world !")


class ChatView(ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def post(self, request):
        input_text = request.data.get('input_text')
        openai.api_key = "api-key"
        output_text = openai.Completion.create(
            engine="text-davinci-003",
            prompt=input_text,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        ).choices[0].text
        # Split the output text based on a specific delimiter (e.g. newline character)
        # output_array = output_text.split('\n')
        # datalist = list(filter(lambda x: len(x) > 0, output_array))
        response = json.loads(output_text)
        print(response)        
        details = ['H1', 'H2', 'MetaTitle', 'Content', 'MetaKeywords', 'MetaMisc']

        output_dict = {}

        for detail in details:
            if int(len(response)) == 6:
                output_dict = response
            elif detail in response:
                output_dict[detail] = response[detail]
            else:
                output_dict[detail] = ""

        print(output_dict)
        chat = Chat.objects.create(input_text=input_text, output_text=output_dict)
        serializer = ChatSerializer(chat)
        return Response(serializer.data)


class PdfUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

from django.shortcuts import render
from django.http import HttpResponse



from django.shortcuts import render,redirect

from django.http import HttpResponse
import json
from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response
from .serializers import TagSerializer

from .models import Tag
import json

from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import serializers

import requests
from bs4 import BeautifulSoup

# Create your views here.
def index(request):
    return HttpResponse('Hello World')

class TagView(ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def post(self, request):
        url = request.data.get('url')
        if not url:
            url = request.query_params.get('url')
        print(url)
        reqs = requests.get(url)
        soup = BeautifulSoup(reqs.text, 'lxml')
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        h3_tags = soup.find_all('h3')
        title_tags = soup.find_all('title')
        backlink_tags = soup.find_all('a')
        description_tags = soup.find_all('meta', attrs={'name': ['description', 'Description']})

        h1_count = len(h1_tags)
        h2_count = len(h2_tags)
        h3_count = len(h3_tags)
        title_count = len(title_tags)
        backlink_count = len(backlink_tags)
        description_count = len(description_tags)

        data = {
            "Number of h1 tags": h1_count,
            "Number of h2 tags": h2_count,
            "Number of h3 tags": h3_count,
            "Number of title tags": title_count,
            "backlink count": backlink_count,
            "Number of description tags": description_count,
           
            "headings": [],
            "Word count": []
        }

        for heading in soup.find_all(["h1", "h2", "h3"]):
            data["headings"].append({"tag": heading.name, "text": heading.text.strip()})

        for bodycount in soup.find_all(["body"]):
            # ["bodycounts"].append({"text": bodycount.text.strip()})
            a = bodycount.text.strip()
            b = (str(len(a.split())))
            data["Word count"] = b 
      

        if h1_count == 0:
            data["h1_status"] = "not_present"
        elif h1_count > 1:
            data["h1_status"] = "more_than_one"
        else:
            data["h1_status"] = "present_once"

        if h2_count == 0:
            data["h2_status"] = "not_present"
        elif h2_count > 1:
            data["h2_status"] = "more_than_one"
        else:
            data["h2_status"] = "present_once"

        if h3_count == 0:
            data["h3_status"] = "not_present"
        elif h3_count > 1:
            data["h3_status"] = "more_than_one"
        else:
            data["h3_status"] = "present_once"

        if title_count == 0:
            data["title_status"] = "not_present"
        elif title_count > 1:
            data["title_status"] = "more_than_one"
        else:
            data["title_status"] = "present_once"

        if backlink_count == 0:
            data["backlink_status"] = "not_present"
        elif backlink_count > 1:
            data["backlink_status"] = "more_than_one"
        else:
            data["backlink_status"] = "present_once"
        
        if description_count == 0:
            data["description_status"] = "not_present"
        elif description_count > 1:
            data["description_status"] = "more_than_one"
        else:
            data["description_status"] = "present_once"

        # serializer = ChatSerializer(data, many=True)
        # data = serializer.data

        # if message:
        #     data['message'] = message

        # return JsonResponse(data, safe=False)
        # return Response(serializer.data)
        print(data)
        chat = Tag.objects.create(url=url, output=data)
        serializer = TagSerializer(chat)
        return Response(serializer.data)




class TagUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]


class DatatagView(ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def post(self, request):
        url = request.data.get('url')
        if not url:
            url = request.query_params.get('url')

        

        try:
            reqs = requests.get(url)
            reqs.raise_for_status()
        except (requests.exceptions.RequestException, ValueError):
            return Response({})

        soup = BeautifulSoup(reqs.text, 'lxml')
        h1_tags = soup.find_all('h1')
        h2_tags = soup.find_all('h2')
        h3_tags = soup.find_all('h3')
        title_tags = soup.find_all('title')
        backlink_tags = soup.find_all('a')
        description_tags = soup.find_all('meta', attrs={'name': ['description', 'Description']})
        
        h1_count = len(h1_tags)
        h2_count = len(h2_tags)
        h3_count = len(h3_tags)
        title_count = len(title_tags)
        backlink_count = len(backlink_tags)
        description_count = len(description_tags)
       
   
        data = {
            "Number of h1 tags": h1_count,
            "Number of h2 tags": h2_count,
            "Number of h3 tags": h3_count,
            "Number of title tags": title_count,
            "backlink count": backlink_count,
            "Number of description tags": description_count,
            "Word count": [],
        }
        

        for bodycount in soup.find_all(['body']):
            a = bodycount.text.strip()
            b = int(str(len(a.split())))
            data["Word count"] = b 

        if h1_count == 0:
            data["h1_status"] = "not_present"
        elif h1_count > 1:
            data["h1_status"] = "more_than_one"
        else:
            data["h1_status"] = "present_once"

        if h2_count == 0:
            data["h2_status"] = "not_present"
        elif h2_count > 1:
            data["h2_status"] = "more_than_one"
        else:
            data["h2_status"] = "present_once"

        if h3_count == 0:
            data["h3_status"] = "not_present"
        elif h3_count > 1:
            data["h3_status"] = "more_than_one"
        else:
            data["h3_status"] = "present_once"

        if title_count == 0:
            data["title_status"] = "not_present"
        elif title_count > 1:
            data["title_status"] = "more_than_one"
        else:
            data["title_status"] = "present_once"

        if backlink_count == 0:
            data["backlink_status"] = "not_present"
        elif backlink_count > 1:
            data["backlink_status"] = "more_than_one"
        else:
            data["backlink_status"] = "present_once"
        
        if description_count == 0:
            data["description_status"] = "not_present"
        elif description_count > 1:
            data["description_status"] = "more_than_one"
        else:
            data["description_status"] = "present_once"

        
        return Response(data)
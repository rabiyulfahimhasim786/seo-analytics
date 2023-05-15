from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world !")


from django.shortcuts import render,redirect

from django.http import HttpResponse
import json
from django.http import HttpResponse, JsonResponse

from rest_framework.response import Response
from .serializers import SitemapapiSerializer

from .models import Sitemapapi

from django.http import Http404
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework import serializers

import json
from pathlib import Path
import numpy as np
import csv
from lxml import etree
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

import requests
from django.db import connections, transaction
from django.core.cache import cache # This is the memcache cache.

def flush():
    # This works as advertised on the memcached cache:
    cache.clear()
    # This manually purges the SQLite cache:
    cursor = connections['cache_database'].cursor()
    cursor.execute('DELETE FROM cache_table')
    transaction.commit_unless_managed(using='cache_database')
    return 'ok'

def index(request):
    return HttpResponse("Hello, world!")

def check_sitemap_urls(baseurls):
    """Attempts to resolve all urls in a sitemap and returns the results

    Args:
        sitemap (str): A URL

    Returns:
        list of tuples: [(status_code, url, msg)].
    """
    results = []
    res = requests.get(baseurls)
    doc = etree.XML(res.content)

    # xpath query for selecting all element nodes in namespace
    query = "descendant-or-self::*[namespace-uri()!='']"
    # for each element returned by the above xpath query...
    for element in doc.xpath(query):
        # replace element name with its local name
        element.tag = etree.QName(element).localname

    # get all the loc elements
    links = doc.xpath(".//loc")
    futures = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for i, link in enumerate(links, 1):
            url = link.text
            futures.append(executor.submit(check_url, url))

    for future in as_completed(futures):
        results.append(future.result())

    # Sort by status
    results.sort(key=lambda result: result[0])

    return results

def check_url(url):
    try:
        print(f"Checking {url}")
        r = requests.get(url)

        if r.history:
            result = (
                r.status_code,
                url,
                "No error. Redirect to " + r.url,
            )
        elif r.status_code == 200:
            result = (r.status_code, url, "No error. No redirect.")
        else:
            result = (r.status_code, url, "Error?")
    except Exception as e:
        result = (0, url, e)

    return result

dot = '.'
# dot = '/var/www/ssl/site'
def main(sitemaps):
    #print(sitemaps)
    for sitemap in sitemaps:
        #print(sitemap)
        results = check_sitemap_urls(sitemap)

        # name = os.path.basename(sitemap).split(".")[0]
        # report_path = Path(f"./media/{name}.csv")
        report_path = Path(f"{dot}/media/csv/data2.csv")
    

        with open(report_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Status_Code", "URL", "Message"])
            for result in results:
                writer.writerow([result[0], result[1], result[2]])
        
    return 'ok'

def Convert(string):
    li = list(string.split(" "))
    return li

class Overallapi(ListCreateAPIView):
    queryset = Sitemapapi.objects.all()
    serializer_class = SitemapapiSerializer

    def post(self, request):
        input_url = request.data.get('xmls')
        if not input_url:
            input_url = request.query_params.get('xmls')

        try:
            sitemapurl = Convert(input_url)
            print(sitemapurl)


            main(sitemapurl)

            file = pd.read_csv(dot+"/media/csv/data2.csv")
            departments = [ 404, 400]
            filterdata=file.loc[file['Status_Code'].isin(departments)]
            headerList = ['Status_Code', 'URL','Message']
            filterdata.to_csv(dot+"/media/csv/data3.csv", header=headerList, index=None, encoding='utf-8')
            filedata = dot+"/media/csv/data3.csv"
            dfjson = pd.read_csv(filedata , index_col=None, header=0)
                            #geeks = df.to_html()
            #json_records = dfjson.reset_index().to_json(orient ='records')
            #data = []
            #data = json.loads(json_records)
            nofilterdfjson = pd.read_csv(dot+"/media/csv/data2.csv", index_col=None, header=0)
                            #geeks = df.to_html()
            #nonfilterjson_records = nofilterdfjson.reset_index().to_json(orient ='records')
            #nonfilterdata = []
            #nonfilterdata = json.loads(nonfilterjson_records)
                        # return render(request, 'index.html',)
                        # main(baseurls)
            # return render(request, 'data.html',{'data': data, 'd': nonfilterdata })

            # Assuming dfjson['URL'].values.tolist() gives you ['link1', 'link2']
            input_list = dfjson['URL'].str.strip().values.tolist()

            # Convert the list to a JSON-formatted string with double quotes
            # broken_data = json.dumps(input_list, ensure_ascii=False)
            broken_data = json.dumps(input_list)

            output_list = nofilterdfjson['URL'].str.strip().values.tolist()

            # Convert the list to a JSON-formatted string with double quotes
            # working_data = json.dumps(output_list, ensure_ascii=False)
            working_data = json.dumps(output_list)
        
            overallseo = Sitemapapi.objects.create(xmls=input_url, brokenlinks=broken_data, workinglinks=working_data)
            # print(output_data)
            # serializer = PageperformanceSerializer(seo)
            serializer = SitemapapiSerializer(overallseo)
            return Response(serializer.data)
                
        except requests.exceptions.HTTPError as http_err:
            # Return an error response with the URL and error message
            error_msg = f"HTTP error occurred: {http_err}"
            error_data = {'url': input_url, 'error': error_msg}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            # Return an error response with the URL and error message
            error_msg = f"An error occurred: {err}"
            error_data = {'url': input_url, 'error': error_msg}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)



class OverallapiUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    queryset = Sitemapapi.objects.all()
    serializer_class = SitemapapiSerializer
    #permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]




class SitemapapiView(ListCreateAPIView):
    serializer_class = SitemapapiSerializer
    queryset = Sitemapapi.objects.all()

    # def post(self, request):
    #     url = request.data.get('url')
    #     if not url:
    #         url = request.query_params.get('url')

        

    #     try:
    #         reqs = requests.get(url)
    #         reqs.raise_for_status()
    #     except (requests.exceptions.RequestException, ValueError):
    #         return Response({})

    #     soup = BeautifulSoup(reqs.text, 'lxml')
    #     h1_tags = soup.find_all('h1')
    #     h2_tags = soup.find_all('h2')
    #     h3_tags = soup.find_all('h3')
    #     title_tags = soup.find_all('title')
    #     backlink_tags = soup.find_all('a')
    #     description_tags = soup.find_all('meta', attrs={'name': ['description', 'Description']})
        
    #     h1_count = len(h1_tags)
    #     h2_count = len(h2_tags)
    #     h3_count = len(h3_tags)
    #     title_count = len(title_tags)
    #     backlink_count = len(backlink_tags)
    #     description_count = len(description_tags)
       
   
    #     data = {
    #         "Number of h1 tags": h1_count,
    #         "Number of h2 tags": h2_count,
    #         "Number of h3 tags": h3_count,
    #         "Number of title tags": title_count,
    #         "backlink count": backlink_count,
    #         "Number of description tags": description_count,
    #         "Word count": [],
    #     }
        

    #     for bodycount in soup.find_all(['body']):
    #         a = bodycount.text.strip()
    #         b = int(str(len(a.split())))
    #         data["Word count"] = b 

    #     if h1_count == 0:
    #         data["h1_status"] = "not_present"
    #     elif h1_count > 1:
    #         data["h1_status"] = "more_than_one"
    #     else:
    #         data["h1_status"] = "present_once"

    #     if h2_count == 0:
    #         data["h2_status"] = "not_present"
    #     elif h2_count > 1:
    #         data["h2_status"] = "more_than_one"
    #     else:
    #         data["h2_status"] = "present_once"

    #     if h3_count == 0:
    #         data["h3_status"] = "not_present"
    #     elif h3_count > 1:
    #         data["h3_status"] = "more_than_one"
    #     else:
    #         data["h3_status"] = "present_once"

    #     if title_count == 0:
    #         data["title_status"] = "not_present"
    #     elif title_count > 1:
    #         data["title_status"] = "more_than_one"
    #     else:
    #         data["title_status"] = "present_once"

    #     if backlink_count == 0:
    #         data["backlink_status"] = "not_present"
    #     elif backlink_count > 1:
    #         data["backlink_status"] = "more_than_one"
    #     else:
    #         data["backlink_status"] = "present_once"
        
    #     if description_count == 0:
    #         data["description_status"] = "not_present"
    #     elif description_count > 1:
    #         data["description_status"] = "more_than_one"
    #     else:
    #         data["description_status"] = "present_once"

        
    #     return Response(data)
    def post(self, request):
        input_url = request.data.get('xmls')
        if not input_url:
            input_url = request.query_params.get('xmls')
        sitemapurl = Convert(input_url)
        try:
            #sitemapurl = Convert(input_url)
            print(sitemapurl)


            main(sitemapurl)

            file = pd.read_csv(dot+"/media/csv/data2.csv")
            departments = [ 404, 400]
            filterdata=file.loc[file['Status_Code'].isin(departments)]
            headerList = ['Status_Code', 'URL','Message']
            filterdata.to_csv(dot+"/media/csv/data3.csv", header=headerList, index=None, encoding='utf-8')
            filedata = dot+"/media/csv/data3.csv"
            dfjson = pd.read_csv(filedata , index_col=None, header=0)
                            #geeks = df.to_html()
            #json_records = dfjson.reset_index().to_json(orient ='records')
            #data = []
            #data = json.loads(json_records)
            nofilterdfjson = pd.read_csv(dot+"/media/csv/data2.csv", index_col=None, header=0)
                            #geeks = df.to_html()
            #nonfilterjson_records = nofilterdfjson.reset_index().to_json(orient ='records')
            #nonfilterdata = []
            #nonfilterdata = json.loads(nonfilterjson_records)
                        # return render(request, 'index.html',)
                        # main(baseurls)
            # return render(request, 'data.html',{'data': data, 'd': nonfilterdata })

            # Assuming dfjson['URL'].values.tolist() gives you ['link1', 'link2']
            input_list = dfjson['URL'].str.strip().values.tolist()

            # Convert the list to a JSON-formatted string with double quotes
            # broken_data = json.dumps(input_list, ensure_ascii=False)
            broken_data = json.dumps(input_list)

            output_list = nofilterdfjson['URL'].str.strip().values.tolist()

            # Convert the list to a JSON-formatted string with double quotes
            # working_data = json.dumps(output_list, ensure_ascii=False)
            working_data = json.dumps(output_list)      
            ## saving in to database  
            #overallseo = Sitemapapi.objects.create(xmls=input_url, brokenlinks=broken_data, workinglinks=working_data)
            # print(output_data)
            # serializer = PageperformanceSerializer(seo)
            #serializer = SitemapapiSerializer(overallseo)
            #return Response(serializer.data)

            ## not saving into database
            data = {
            "xmls": input_url,
            "brokenlinks": broken_data,
            "workinglinks": working_data,
            }
            return Response(data)
                
        except requests.exceptions.HTTPError as http_err:
            # Return an error response with the URL and error message
            error_msg = f"HTTP error occurred: {http_err}"
            error_data = {'url': input_url, 'error': error_msg}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

        except Exception as err:
            # Return an error response with the URL and error message
            error_msg = f"An error occurred: {err}"
            error_data = {'url': input_url, 'error': error_msg}
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render
import json
# Create your views here.
from django.http import HttpResponse
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from .models import Sitemapxml
from .forms import SitemapxmlForm
import advertools as adv
import pandas as pd
import requests
from django.core.cache import cache
cache.set('my_key', 'hello, world!', 30)
cache.get('my_key')
cache.clear()
def index(request):
    return HttpResponse("Hello, world !")

dot = '.'
def sitemap_xml_data(request):
    if request.method == 'POST':
        form = SitemapxmlForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # return redirect('index')
            documents = Sitemapxml.objects.all()
            for obj in documents:
                baseurls = obj.url
            print(baseurls)
            sigortam = adv.sitemap_to_df(baseurls)
            # sigortam = adv.sitemap_to_df('https://trophydeals.com/sitemap.xml')
            sigortam.to_csv(dot+'/media/csv/crawled_sitemap.csv', index = False)
            sigortam = pd.read_csv(dot+'/media/csv/crawled_sitemap.csv')
            # sigortam.head(5)
            url_status = []
            url_message = []
            for url in sigortam['loc']:
                resp = requests.get((url))
                resp.status_code
                try:
                    print('start')
                    if  400 <= resp.status_code < 500:
                        # url_status.append((url, resp.status_code))
                        # url_status.append(str(resp.status_code) + resp.reason)
                        url_status.append(resp.status_code)
                        url_message.append(resp.reason)
                    elif 300 <= resp.status_code < 400:
                        url_status.append(resp.status_code)
                        url_message.append(resp.reason)
                    elif 500 < resp.status_code < 600:
                        url_status.append(resp.status_code)
                        url_message.append(resp.reason)
                    else:
                        url_status.append(resp.status_code)
                        url_message.append(resp.reason)
                except requests.exceptions.RequestException as e:
                        print(url + " is inactive with error " + str(e) + ".")
                        statuscodesdata = " is inactive with error " + str(e) + "."
                        url_status.append(statuscodesdata)
                        url_message.append(resp.reason)
            sigortam['status'] = url_status
            d1 = {'Url': sigortam['loc'], 'Statuscode': url_status, 'Statusreason':url_message, }
            dataframes = pd.DataFrame(data=d1)
            dataframes.to_csv(dot+'/media/csv/data.csv', index=False)
            file = pd.read_csv(dot+"/media/csv/data.csv")
            departments = [100, 101, 102, 103, 300, 301, 302, 303, 304, 305, 306, 307, 308, 400, 401, 402, 403, 404, 500, 600,]
            filterdata=file.loc[file['Statuscode'].isin(departments)]
            headerList = ['Domainname', 'Statuscode','Domainstatus']
            filterdata.to_csv(dot+"/media/csv/data1.csv", header=headerList, index=None, encoding='utf-8')
            filedata = dot+"/media/csv/data1.csv"
            dfjson = pd.read_csv(filedata , index_col=None, header=0)
            #geeks = df.to_html()
            json_records = dfjson.reset_index().to_json(orient ='records')
            data = []
            data = json.loads(json_records)
            nofilterdfjson = pd.read_csv(dot+'/media/csv/data.csv', index_col=None, header=0)
            #geeks = df.to_html()
            nonfilterjson_records = nofilterdfjson.reset_index().to_json(orient ='records')
            nonfilterdata = []
            nonfilterdata = json.loads(nonfilterjson_records)
            # sigortam[['loc', 'status']].to_csv(dot+'/media/csv/data.csv', index=False)
            # df.to_csv(dot+'/media/csv/data.csv', index=False)
            # df.to_csv(dot+'media/data.csv', index = False)
            return render(request, 'form_upload.html', {'data': data, 'd': nonfilterdata })
    else:
        form = SitemapxmlForm()
        documents = Sitemapxml.objects.all()
    return render(request, 'form_upload.html', {
        'form': form
    })



def metatag(request):
    return render(request, 'index.html')


def content(request):
    return render(request, 'embded.html')
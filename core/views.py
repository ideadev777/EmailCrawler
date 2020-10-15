from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from email_scraper import scrape_emails
from urllib.request import Request, urlopen
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl
import re
import urllib.request
from django.views import generic


# Create your views here.
"""
def index(request):
    template = loader.get_template('index.html')
    urlList = str(request.GET.get('url')).split(',')
    mailList = str(request.GET.get('mail')).split(',')
    dataList = []
    num = len(urlList)
    if num == len(mailList) :
        for i in range(0,num) :
            url = urlList[i]
            if url == "None" :
                continue
            if len(url) == 0 : 
                continue
            print('Hi '+urlList[i])
            info = {'url':url,'email':mailList[i]}
            dataList.append(info)
    print(len(dataList))
    context = {
        'dataList' : dataList,
    }
    
"""

class Index(generic.View):
    template = loader.get_template('index.html')
    def get(self,*args,**kwargs):
        context = {

        }
        return HttpResponse(self.template.render(context,self.request))
#    @csrf_exempt
    def post(self,*args,**kwargs):
        urlList = self.request.POST.get('urlField').split(',')
        print(urlList)
        print('>>>>>>>>>>>>>>>>')
        print(self.request.POST.get('emailField'))
        emailList = self.request.POST.get('emailField').split(',')
#        emailList = re.split('[|]',self.request.POST.get('emailField'))
        print(emailList)
        dataList = []
        num = len(urlList)
        print(str(num)+' '+str(len(emailList)))
        if num == len(emailList) :
            for i in range(0,num) :
                url = urlList[i]
                print(url)
                if url == "None" :
                    continue
                if len(url) == 0 :
                    continue
                info = {'url':url,'email':emailList[i]}
                dataList.append(info)
        print(dataList)
        context = {
            'dataList' : dataList,
        }
        return HttpResponse(self.template.render(context,self.request))

@csrf_exempt
@api_view(['POST'])
def collect(request):
    urlList = str(request.POST['urlList']).splitlines()
    retUrlList = []
    retMailList = []
    dataList = []
    for url in urlList :
        if len(url) == 0 :
            continue
        url = url.replace(' ','')
        retUrlList.append(url)
        try:
#            retMailList.append("ret")
#            continue

            print(url)
            r = urllib.request.Request(url, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
            html = urllib.request.urlopen(r)
            soup = BeautifulSoup(html, 'html.parser')
            emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", str(soup))
            print(emails)
            strEmail = ""
            mySet = []
            for email in emails :
                if email in mySet :
                    continue
                mySet.append(email)
                strEmail = strEmail + '    ' + email
            retMailList.append(strEmail)
#            retMailList.append(str(emails))
        except:
            retMailList.append(" ")
            pass            
    data = {
        'url':retUrlList,
        'mail':retMailList,
        }
    return Response(data,status=status.HTTP_200_OK)

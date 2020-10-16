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
from .googling import *

class Index(generic.View):
    template = loader.get_template('index.html')
    def get(self,*args,**kwargs):
        context = {

        }
        return HttpResponse(self.template.render(context,self.request))
#    @csrf_exempt
    def post(self,*args,**kwargs):
        print(">>>>>>>>>>>>>>>>> Post <<<<<<<<<<<<<")
        urlList = self.request.POST.get('urlField').split(',')
        emailList = self.request.POST.get('emailField').split(',')
        occurList = self.request.POST.get('occurField').split(',')
        queryList = self.request.POST.get('queryField').split(',')
        print('Occurlist = ')
        print(occurList)
        dataList = []
        num = len(urlList)
        keywordCnt = len(queryList)
        step = 0
        if num == len(emailList) :
            for i in range(0,num) :
                url = urlList[i]
                print(url)
                if url == "None" :
                    continue
                if len(url) == 0 :
                    continue
                info = {'url':url,'email':emailList[i]}
                occur = []
                for i in range(step,step+keywordCnt):
                    occur.append(occurList[i])
                step = step + keywordCnt
                info['occurList'] = occur
                dataList.append(info)
        print(dataList)
        context = {
            'query' : queryList,
            'dataList' : dataList,
        }
        return HttpResponse(self.template.render(context,self.request))

@csrf_exempt
@api_view(['POST'])
def collect(request):
    urlList = str(request.POST['urlList']).splitlines()
#    print('collect started:::: ' + urlList)
    query = str(request.POST['keywords']).split(' ')
    queryCnt = len(query)
#    print('keywords are ' +query)
    retUrlList = []
    retMailList = []
    dataList = []
    keywordList = []
    for key in query :
        if key in keywordList:
            continue
        if len(key) < 3 :
            continue
        keywordList.append(key)
    print(keywordList)
    occurList = []
    for url in urlList :
        if len(url) == 0 :
            continue
        url = url.replace(' ','')
        retUrlList.append(url)
        try:
            print("Bot on ::::::::::::: " + url)
            ret = RecursiveSearch( url, 3, keywordList )
            print(ret['emailList'])
            strEmail = ""
            for email in ret['emailList'] :
                strEmail = strEmail + '    ' + email
            retMailList.append(strEmail)
            cnt = len(ret['occurList'])
            print('Count ' + str(cnt))
            if cnt != queryCnt:
                for i in range(1,queryCnt+1) :
                    occurList.append(0)
            else:
                for occur in ret['occurList'] :
                    occurList.append(occur)
        except:
            retMailList.append(" ")
            pass            
    data = {
        'url':retUrlList,
        'mail':retMailList,
        'occurList' : occurList,
        'query' : query,
        }
    return Response(data,status=status.HTTP_200_OK)

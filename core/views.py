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
        queryListTmp = self.request.POST.get('queryField').split(',')
        queryList = []
        for q in queryListTmp:
            if len(q) :
                queryList.append(q)
        maxOccurUrlList = self.request.POST.get('maxUrlField').split(',')
        dataList = []
        num = len(urlList)
        print(num)
        keywordCnt = len(queryList)
        print(keywordCnt)
        print("*****************************")
        print(urlList)
        print(emailList)
        print(occurList)
        print(queryList)
        print(maxOccurUrlList)
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
                for j in range(step,step+keywordCnt):
                    occur.append(occurList[j])
                step = step + keywordCnt
                info['occurList'] = occur
                info['maxOccurUrl'] = maxOccurUrlList[i]
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
    queryTmp = str(request.POST['keywords']).split(' ')
    maxPageCount = int(request.POST['pagecount'])
    collectMail = False
    print(str(request.POST['collectemail']))
    if str(request.POST['collectemail']) == "true" :
        collectMail = True
    query = []
    for q in queryTmp:
        if len(q) :
            query.append(q)
    queryCnt = len(query)
#    print('keywords are ' +query)
    retUrlList = []
    maxOccurUrlList = []
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
            ret = RecursiveSearch( url, maxPageCount, keywordList,collectMail )
            print(ret['emailList'])
            strEmail = ""
            for email in ret['emailList'] :
                strEmail = strEmail + '    ' + email
            retMailList.append(strEmail)
            maxOccurUrlList.append(ret['maxOccurUrl'])
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
        'maxOccurUrlList' : maxOccurUrlList,
        }
    return Response(data,status=status.HTTP_200_OK)

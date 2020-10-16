import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
import urllib.request
import re


colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()
keywordList = []
usageList = []

def is_valid(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def get_all_website_links(url):
    urls = set()
    try:
        domain_name = urlparse(url).netloc
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        r = urllib.request.Request(url, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
        html = urllib.request.urlopen(r)
        soup = BeautifulSoup(html, 'html.parser')
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
            if not is_valid(href):
                continue
            if href in internal_urls:
                continue
            if domain_name not in href:
                continue
            urls.add(href)
            internal_urls.add(href)
    except:
        pass
    return urls

total_urls_visited = 0
max_internal_urls = 10

def crawl(url, max_urls=5):
    if len(internal_urls) > max_internal_urls :
        return
    global total_urls_visited
    total_urls_visited += 1
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls=max_urls)

def RecursiveSearch( url, maxCnt, query ):
    global total_urls_visited
    global max_internal_urls
    total_urls_visited = 0
    max_internal_urls = maxCnt

    occurList = []
    keyCount = len(query)
    for i in range(0,keyCount) :
        occurList.append(0)

    internal_urls.clear()
    external_urls.clear()
    emailList = []
    todoList = []

    crawl(url)
    for var in internal_urls :
        todoList.append(var)
        maxCnt = maxCnt - 1
        if maxCnt < 0 :
            break
    if url not in todoList:
        todoList.append(url)
    maxOccur = 0
    maxOccurUrl = url
    for url in todoList :
        try:
            print("start parse >>>>>>>" + url)
            r = urllib.request.Request(url, headers= {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'})
            html = urllib.request.urlopen(r)
            soup = BeautifulSoup(html, 'html.parser')
            content = soup.get_text()
            content.replace('\n','')
            emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", content)
#            print(content)
            content = content.lower()
            tot = 0
            for i in range(0,keyCount) :
                k = content.count(query[i].lower())
                occurList[i] = occurList[i] + k
                tot = tot + k
            if tot > maxOccur :
                maxOccur = tot
                maxOccurUrl = url
            for email in emails :
                if email in emailList:
                    continue
                emailList.append(email)            
        except:
            pass
    ret = {
        "emailList" : emailList,
        "occurList" : occurList,
        'maxOccurUrl' : maxOccurUrl,
        }
    print('##########END########')
    return ret

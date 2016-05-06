
# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
from urlparse import urljoin

class CarePeoplePage:
    def __init__(self, url, cookie):        
        header = { 
                   'Connection' : 'keep-alive', 
                   'cookie' : cookie, 
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0' 
                 }
        
        self.__fristPageUrl = url
        self.__headers = header
        self.__pageTotalNum = 0
        
        request = urllib2.Request(url, headers=self.__headers) 
        try:
            content =urllib2.urlopen(request)
        except:
            print 'Network Error'
            return
    
        pageContent = content.read()
        
        #soup = BeautifulSoup(pageContent)
        #pageName = 'CarePeoplePage.txt'
        #fp = open(pageName, 'w')
        #fp.write(soup.prettify().encode('utf-8'))
        #fp.close()
        
        self.__pageTotalNum = self.__GetNextPageTotalNum(pageContent)
        if (self.__pageTotalNum == 0):
            self.__pageTotalNum = 1
        
    def GetPageTotalNum(self):
        return self.__pageTotalNum
        
    def GetPeopleList(self, pageIndex):
        
        peopleList = []
        if (pageIndex < 1 or pageIndex > self.__pageTotalNum):
            return peopleList
        
        url = ''
        if (pageIndex == 1):
            url = self.__fristPageUrl
        else:
            url = self.__fristPageUrl
            url += '?page='
            url += str(pageIndex)
           
        request = urllib2.Request(url, headers=self.__headers) 
        try:
            content =urllib2.urlopen(request)
        except:
            print 'Network Error'
            return peopleList
    
        pageContent = content.read()
        peopleList = self.__GetPeoplesFromPage(pageContent)
        
        return peopleList
        
    def __GetPeoplesFromPage(self, pageContent):
        peopleList = []
        
        soup = BeautifulSoup(pageContent)
        tableList = soup('table') 
        for table in tableList:
            tdList = table('td')
            if len(tdList) != 2 :
                continue
            td = tdList[1]
            link = td.a
            
            if ('href' in dict(link.attrs)):
                url = link['href']
                peopleList.append([link.string.encode('utf-8'), url.encode('utf-8')])
        
        return peopleList
    
    def __GetNextPageTotalNum(self, pageContent):
        soup = BeautifulSoup(pageContent)
        divList = soup('div') 
        for div in divList:
            divAttrs = div.attrs
        
            if (not divAttrs.has_key('class') or not divAttrs.has_key('id')):
                continue
            if (divAttrs['class'] != ['pa'] or divAttrs['id'] != 'pagelist'):
                continue
        
            inputList = div('input')
            for input in inputList:
                inputAttrs = input.attrs
                if (not inputAttrs.has_key('name') or 
                    not inputAttrs.has_key('type') or
                    not inputAttrs.has_key('value')):
                    continue
            
                num = inputAttrs['value']
                return int(num)
            
        return 0   
    
class PeoplePage:
    def __init__(self, url, cookie):
        header = { 
                   'Connection' : 'keep-alive', 
                   'cookie' : cookie, 
                   'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0' 
                 }
        
        self.__fristPageUrl = url
        self.__headers = header
        self.__blogPageTotalNum = 0
        self.__carePeoplePageUrl = ''
        
        request = urllib2.Request(url, headers=self.__headers) 
        try:
            content =urllib2.urlopen(request)
        except:
            print 'Network Error'
            return
    
        pageContent = content.read()
        
        #soup = BeautifulSoup(pageContent)
        #fp = open('xienapage.txt', 'w')
        #fp.write(soup.prettify().encode('utf-8'))
        #fp.close()
        
        self.__blogPageTotalNum = self.__GetBlogPageTotalNum(pageContent)
        if (self.__blogPageTotalNum == 0):
            self.__blogPageTotalNum = 1
            
        self.__carePeoplePageUrl = self.__GetCarePeoplePageUrl(pageContent)
    
    def GetPeopleData(self):
        pass
    
    def GetCarePeoplePageUrl(self):
        return self.__carePeoplePageUrl
    
    def GetBlogPageTotalNum(self):
        return self.__blogPageTotalNum
    
    def GetBlogList(self, pageIndex):
        
        blogList = []
        if (pageIndex < 1 or pageIndex > self.__blogPageTotalNum):
            return blogList
        
        url = ''
        if (pageIndex == 1):
            url = self.__fristPageUrl
        else:
            url = self.__fristPageUrl
            url += '?page='
            url += str(pageIndex)
            
        request = urllib2.Request(url, headers=self.__headers) 
    
        try:
            content =urllib2.urlopen(request)
        except:
            print('Network Error')
            return blogList
            
        pageContent = content.read()
        blogList = self.__GetBlogsFromPage(pageContent)
        
        return blogList
    
    def __GetBlogPageTotalNum(self, pageContent):
        soup = BeautifulSoup(pageContent)
        divList = soup('div') 
        for div in divList:
            divAttrs = div.attrs
        
            if (not divAttrs.has_key('class') or not divAttrs.has_key('id')):
                continue
            if (divAttrs['class'] != ['pa'] or divAttrs['id'] != 'pagelist'):
                continue
        
            inputList = div('input')
            for input in inputList:
                inputAttrs = input.attrs
                if (not inputAttrs.has_key('name') or 
                    not inputAttrs.has_key('type') or
                    not inputAttrs.has_key('value')):
                    continue
            
                num = inputAttrs['value']
                return int(num)
            
        return 0
        
    def __GetBlogsFromPage(self, pageContent):
        soup = BeautifulSoup(pageContent)
    
        blogList = []
    
        divList = soup('div') 
        for div in divList:
            divAttrs = div.attrs
        
            if (not divAttrs.has_key('class') or not divAttrs.has_key('id')):
                continue
            if (divAttrs['class'] != ['c']):
                continue

            blogId = divAttrs['id']
            blogText = ''
            blogTime = ''
        
            spanList = div('span')
            for span in spanList:
                spanAttrs = span.attrs
            
                if (not spanAttrs.has_key('class')):
                    continue
                if (spanAttrs['class'] != ['ctt'] and spanAttrs['class'] != ['cmt'] and spanAttrs['class'] != ['ct']):
                    continue
            
                if (blogText == '' and (spanAttrs['class'] == ['ctt'] or spanAttrs['class'] == ['cmt'])):
                    for string in span.strings:
                        blogText += string
            
                if (spanAttrs['class'] == ['ct']):
                    for string in span.strings:
                        blogTime += string
                        
        
            try:
                blogList.append([blogId.encode('utf-8'), blogText.encode('utf-8'), blogTime.encode('utf-8')])
            except:
                continue
        
        return blogList
    
    def __GetCarePeoplePageUrl(self, pageContent):
        url = ''
        
        soup = BeautifulSoup(pageContent)
        divList = soup('div') 
        for div in divList:
            divAttrs = div.attrs
        
            if (not divAttrs.has_key('class')):
                continue
            if (divAttrs['class'] != ['u']):
                continue
                
            subDivList = div('div')
            
            for subDiv in subDivList:
                subDivAttrs = subDiv.attrs
                if (not subDivAttrs.has_key('class')):
                    continue
                if (subDivAttrs['class'] != ['tip2']):
                    continue
                
                link = subDiv.a
                if ('href' in dict(link.attrs)):
                    url = urljoin(self.__fristPageUrl, link['href'])
                    return url.encode('utf-8')
                
        return url
        
cookie ='_T_WM=34fdb0229023a2bbbd2158fce59ed838; gsid_CTandWM=4uwqCpOz5ww7kYKE3XERJ7wJCfE; SUB=_2A256KCs1DeRxGedJ4lYQ8yzFzDyIHXVZ0rV9rDV6PUJbstBeLWSjkW1LHes6Y6ovTsH2R8ML9DC_bVPh663_zw..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5HzJx-7GkUYjF5QwMzUTFb5JpX5o2p5NHD95QpS0.XeKeE1KM7; SUHB=06ZEzPJPka9KET; SSOLoginState=1462524773'   
url = 'http://weibo.cn/xiena'

people = PeoplePage(url, cookie)
carePageUrl = people.GetCarePeoplePageUrl()

carePeoplePage = CarePeoplePage(carePageUrl, cookie)
totalNum = carePeoplePage.GetPageTotalNum()

fp = open('CarePeople.txt', 'wb')
for i in range(1, totalNum + 1):
    peopleList = carePeoplePage.GetPeopleList(i)
    for people in peopleList:
        line = people[0]
        line += '\t'
        line += people[1]
        while (len(line) < 254):
            line += ' '
        line += '\n\n'
        fp.write(line)
        #fp.write(people[0])
        #fp.write('  ')
        #fp.write(people[1])
        #fp.write('  ')
        #fp.write('\n')
        #fp.write('\n')

fp.close()

fp = open('CarePeople.txt', 'rb')
fp.seek(256)
newLine = fp.read(256)
print newLine.decode('utf-8')
#blogList = people.GetBlogList(1)
#weiboName = 'xiena.txt'
#fp = open(weiboName, 'w')
#for blog in blogList:
    #fp.write(blog[0])
    #fp.write('  ')
    #fp.write(blog[1])
    #fp.write('  ')
    #fp.write(blog[2])
    #fp.write('\n')
    #fp.write('\n')
          
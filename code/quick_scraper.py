import scrapy
from bs4 import BeautifulSoup
import sys
import os
import _pickle as pickle
import pandas as pd
from .title_scrape import *
import datetime
class ContentSpider(scrapy.Spider):
    name = "yolo"
    handle_httpstatus_list = [i for i in range(400,500) if i!=200]
    BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    date_=None
    file=None
    url=None
    total_urls=0
    counter=0
    fault_log=None
    ##these variables store the content scraped
    b={}
    date={}
    contents={}
    total_links={}
    NEWS={'reuters.com':sc_reuters,'thehindu.com':sc_thehindu,'economictimes.indiatimes':sc_econt,
    'moneycontrol.com':moneyControl,'ndtv.com':ndtv,'hindubusinessline.com':hindu_bl}
    DATA_DIR = os.path.join(os.getcwd(),'..','data')
    #initialises the data types with the respective keys and empty list/dictionary
    for key in NEWS:
        date[key]=[]
        b[key]={}
        contents[key]=[]
        total_links[key]=[]
    #generates all the links to be scraped 
    def start_requests(self):
        print("\n\nEnter company name to scrape content for")
        cos=[i.split('_')[1] for i in list_files('links/finallinks')]
        print('\n'+str(cos))
        self.dest_file=input()
        try:
            os.mkdir('content/logs/')
        except:
            pass
        today='_'.join(datetime.datetime.today().ctime().split())
        self.fault_log=open(os.path.join(DATA_DIR,'content/logs/'+self.dest_file+'_log_'+today+'.data','w+'))
        for file_name in list_files('links/finallinks'):
            if(self.dest_file.lower() in file_name.lower()):
                tracker(file_name)
                print("SCRAPING DATA FOR "+file_name)
                links = [line.rstrip('\n') for line in open(os.path.join(DATA_DIR,'links/finallinks/'+file_name)) if line!='\n']
                self.total_urls=len(links)
                self.file=file_name
                for l in links:
                    try:
                        self.date_,self.url=l.split('::')
                        request=scrapy.Request(self.url,self.parse,dont_filter=True)
                        request.meta['date']=self.date_
                    except Exception as e:
                        self.fault_log.write(self.date_+'::'+self.url+'\n')
                        self.counter+=1
                        continue
                    yield request
    # gets called at the end when all the data has been scraped .
    # It maintains the same folder format for data storage as before.
    def writeTo(self):
        company=self.dest_file
        for webp in self.date:
            make_directory(company,webp)
            with open(os.path.join(DATA_DIR,'content/'+company+'/'+webp+'/raw_'+self.file.split('.data')[0]+'_'+webp+'.pkl'), 'wb') as fp:
                pickle.dump(self.b[webp], fp)
            temp = {'date':self.date[webp],
                    'data':self.contents[webp],
                    'url':self.total_links[webp]
                    }
            df = pd.DataFrame(temp)
            df.set_index('date',inplace=True)
            df.to_pickle(os.path.join(DATA_DIR,'content/'+company+'/'+webp+'/'+self.file.split('.data')[0]+'_'+webp+'_content.pkl'))
            df.to_csv(os.path.join(DATA_DIR,'content/'+company+'/'+webp+'/'+self.file.split('.data')[0]+'_'+webp+'_content.csv'))
        

    def parse(self, response):
        if(response.status !=200):
            self.counter+=1
            self.fault_log.write(response.meta['date']+'::'+self.url+'\n')
        else:
            self.counter+=1
        for key in self.NEWS:
            if key in response.url:
                print("FETCHING -",response.url)
                bs=BeautifulSoup(response.text,'html.parser')
                content=self.NEWS[key](bs)
                str1=''
                tokens=[]
                for text in content:
                    tokens.extend(text)
                for tk in tokens:
                    str1+=''.join(tk)
                c = datetime.datetime.strptime(response.meta['date'], '%d-%b-%Y')
                if(len(tokens)>0):
                    #yield self.logger.info("date -"+str(c)+" #"*15)
                    self.date[key].append(c)
                    self.contents[key].append(str1)
                    self.total_links[key].append(response.url)
                    temp_={c:str1}
                    self.b[key].update(temp_)
                else:
                    self.fault_log.write(str(c)+'::'+response.url+'\n')
                yield self.logger.info("COUNTER -"+str(self.counter)+" #"*15)
                yield self.logger.info("TOTAL URLS -"+str(self.total_urls)+" #"*12)
                if(self.counter==self.total_urls):
                    self.writeTo() 
                    self.fault_log.close()
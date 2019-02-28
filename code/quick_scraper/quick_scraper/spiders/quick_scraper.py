import scrapy
from bs4 import BeautifulSoup
import sys
import os
import _pickle as pickle
import pandas as pd
from .scrape_with_bs4 import *
import datetime
import os

DATA_DIR = os.path.join(os.getcwd(),'..','..','data')
print(DATA_DIR,"$4$"*10)
class ContentSpider(scrapy.Spider):
    name = "yolo"
    handle_httpstatus_list = [i for i in range(400,500) if i!=200]
    # BASE_PATH = os.path.dirname(os.path.abspath(__file__))
    date_=None
    file=None
    url=None
    total_urls=0
    counter=0
    fault_log=None
    ##these variables store the content scraped
    date={}
    contents={}
    titles={}
    total_links={}
    cs = ContentScrape()
    ts = TitleScrape()
    NEWS_C={'reuters.com':cs.reuters,'thehindu.com':cs.thehindu,'economictimes.indiatimes':cs.econt,
    'moneycontrol.com':cs.moneyControl,'ndtv.com':cs.ndtv,'hindubusinessline.com':cs.hindu_bl}
    NEWS_T = {'reuters.com':ts.reuters,'thehindu.com':ts.thehindu,'economictimes.indiatimes':ts.econt,
    'moneycontrol.com':ts.moneyControl,'ndtv.com':ts.ndtv,'hindubusinessline.com':ts.hindu_bl}

    #initialises the data types with the respective keys and empty list/dictionary
    #stores both title and content
    for key in NEWS_C:
        date[key]=[]
        # b[key]={}
        contents[key]=[]
        titles[key] = []
        total_links[key]=[]
    #generates all the links to be scraped 
    def start_requests(self):
        print("\n\nEnter company name to scrape content for")
        # print("")
        print("Output DIRECTORY:",os.getcwd())
        link_path = os.path.join(DATA_DIR,'links','finallinks')
        cos=[i.split('_')[1] for i in list_files(link_path)]
        print('\n'+str(cos))
        self.dest_file=input()
        try:
            os.mkdir(os.path.join(DATA_DIR,'content/logs/'))
        except:
            pass
        today='_'.join(datetime.datetime.today().ctime().split())
        self.fault_log=open(os.path.join(DATA_DIR,'content/logs/'+self.dest_file+'_log_'+today+'.data'),'w+')
        for file_name in list_files(os.path.join(DATA_DIR,'links/finallinks')):
            if(self.dest_file.lower() in file_name.lower()):
                tracker(file_name,DATA_DIR)
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
            data_dump_dir = os.path.join(DATA_DIR,'content',company,webp)
            if(not os.path.exists(data_dump_dir)):
                os.makedirs(data_dump_dir)
            temp = {'date':self.date[webp],
                    'title':self.titles[webp],
                    'content':self.contents[webp],
                    'url':self.total_links[webp],
                    }
            with open(os.path.join(DATA_DIR,'content/'+company+'/'+webp+'/raw_'+self.file.split('.data')[0]+'_'+webp+'.pkl'), 'wb') as fp:
                pickle.dump(temp, fp)
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
        for key in self.NEWS_C:
            #checks which website does the current url belong to
            if key in response.url:
                print("FETCHING -",response.url)
                bs=BeautifulSoup(response.text,'html.parser')
                #Gets title
                title=self.NEWS_T[key](bs)
                title=self.getString(title)
                #Gets content
                content=self.NEWS_C[key](bs)
                content = self.getString(content)
                #Gets date
                c = datetime.datetime.strptime(response.meta['date'], '%d-%b-%Y')
                if(len(title)>0 or len(content)>0):
                    #yield self.logger.info("date -"+str(c)+" #"*15)
                    self.date[key].append(c)
                    self.titles[key].append(title)
                    self.contents[key].append(content)
                    self.total_links[key].append(response.url)
                else:
                    self.fault_log.write(str(c)+'::'+response.url+'\n')
                yield self.logger.info("COUNTER -"+str(self.counter)+" #"*15)
                yield self.logger.info("TOTAL URLS -"+str(self.total_urls)+" #"*12)
                if(self.counter==self.total_urls):
                    self.writeTo() 
                    self.fault_log.close()

    def getString(self,nested_list):
        str1=''
        tokens=[]
        for text in nested_list:
            tokens.extend(text)
        for tk in tokens:
            str1+=''.join(tk)
        return str1
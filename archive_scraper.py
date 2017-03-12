from bs4 import BeautifulSoup
import requests
import datetime
import lxml
import os
import time
from lxml import html
'''
	 the starting and ending dates are inclusive
'''
class Archive_Scraper:
	def __init__(self):
		print("#"*8+" Enter the details to scrape separated by SPACE.")
		sd,sm,sy=input("Enter starting day month year ").split(" ")
		ed,em,ey=input("Enter ending day month year ").split(" ")
		self.keyword=input("Enter company data to scrape -")
		self.sm=int(sm)
		self.sy=int(sy)
		self.em=int(em)
		self.ey=int(ey)
		self.sd=int(sd)
		self.ed=int(ed)
		print("Scraping from Economictimes")
		#self.econ_times()
		print("Scraping from reuters")
		#self.reuters()
		print("Scraping from thehindu")
		self.thehindu()
	def generate_ym_pair(self,y,sm,em,need_zero):
		year_mon=[]
		for m in range(sm,em+1):
			if(m<10):
				if(need_zero):
					year_mon.append((y,"0"+str(m)))
				else:
					year_mon.append(y,str(m))
			else:
				year_mon.append((y,m))
		return year_mon

	def year_m(self,non_zero):
		year_month=[]
		for y in range(self.sy,self.ey+1):
			if(self.sy==self.ey):
					year_month.extend(self.generate_ym_pair(y,self.sm,self.em,non_zero))
			if(self.sy!=self.ey):
					if(y==self.sy):
						year_month.extend(self.generate_ym_pair(y,self.sm,12,non_zero))
					elif (y==self.ey):
						year_month.extend(self.generate_ym_pair(y,1,self.em))
					else:
						year_month.extend(self.generate_ym_pair(y,1,12))
		return year_month

	def reuters(self):
		url="http://www.reuters.com/resources/archive/us/{year}{month}{date}.html"
		blacklist=['video','#top']
		collection=[]
		year_month=self.year_m(True)
		for year,month in year_month:
			print("Year " + str(year)," Month " +str(month))
			for d in range(self.sd,self.ed+1):
				print ("date "+str(d))
				if(d<10):
					d="0"+str(d)
				r=requests.get(url.format(year=year,month=month,date=d))
				if(r.status_code==200):
					b=BeautifulSoup(r.content,'html.parser')
					links=b.select('div > div > div > div > div > div > a')
					for link in links:
						if(not ([i for i in blacklist if link.get('href').find(i)!=-1])):
							if( link.get('href').find(self.keyword)!=-1):
								index=link.get('href').rfind('/')
								link="http://www.reuters.com/article"+link.get('href')[index:]
								collection.append((str(d)+"-"+str(month)+"-"+str(year),link))
						#else:
						#	print('blacklisted '+link.get('href'))
				else:
					print("Skipped "+r.content)
		
		
		print("Collected "+str(len(collection))+" urls for "+self.keyword)
		self.writeToFile(collection,"reutersArchive",self.keyword,self.sd,self.sm,self.sy)

	def econ_times(self):
		base_url="http://economictimes.indiatimes.com/archivelist/year-{year},month-{month},starttime-{start_t}.cms"
		start_time=36892
		start_date=datetime.date(self.sy,self.sm,self.sd)
		days=(start_date-datetime.date(2001,1,1)).days + start_time
		count_days=(datetime.date(self.ey,self.em,self.ed)-start_date).days+1
		collection=[]
		visit_url=''
		for day in range(count_days):
			date_diff=datetime.timedelta(day)
			final_date=date_diff+start_date
			print (final_date),
			visit_url=base_url.format(year=final_date.year,month=final_date.month,start_t=days+day)
			page=requests.get(visit_url)
			print(visit_url)
			xtree=html.fromstring(page.content)
			links=xtree.xpath("*//section[@id='pageContent']//li/a/@href")
			for link in links:
				if(link.find(self.keyword)!=-1):
					link='http://economictimes.indiatimes.com'+link
					collection.append((str(final_date.day)+'-'+str(final_date.month)+'-'+str(final_date.year),link))
		print("Collected "+str(len(collection))+" urls for "+self.keyword)
		self.writeToFile(collection,"econtimesArchive",self.keyword,self.sd,self.sm,self.sy)

	def thehindu(self):
		base_url="http://www.thehindu.com/archive/web/{year}/{month}/{day}/"
		year_month=self.year_m(True)
		start_date=datetime.date(self.sy,self.sm,self.sd)
		count_days=(datetime.date(self.ey,self.em,self.ed)-start_date).days+1
		for d in range(count_days):
			date_diff=datetime.timedelta(d)
			final_date=date_diff+start_date
			print (final_date),
			visit_url=base_url.format(year=final_date.year,month=final_date.month,day=final_date.day)
			# this webpage loads very slow and becomes unresponsive sometimes hence a timeout of None
			page=requests.get(visit_url,timeout=None)
			print(visit_url)
			xtree=html.fromstring(page.content)
			collection=[]
			links=xtree.xpath("*//ul[@class='archive-list']//a/@href")
			for link in links:
				if(link.find(self.keyword)!=-1):
					collection.append((str(final_date.day)+'-'+str(final_date.month)+'-'+str(final_date.year),link))
		print("Collected "+str(len(collection))+" urls for "+self.keyword)
		self.writeToFile(collection,"thehinduArchive",self.keyword,self.sd,self.sm,self.sy)

	def writeToFile(self,links,webp,company,date,month,year):
		BASE_PATH = os.path.dirname(os.path.abspath(__file__))
		try:
			os.makedirs('links')
		except Exception as e:
			pass
		
		f = open(os.path.join(BASE_PATH,"links","results_"+webp+"_"+company+"_"+str(date)+"_"+str(month)+"_"+str(year)+'.data'),'a+')
		for i,j in links:
			f.write(str(i)+"::"+str(j)+"\n")
		f.close()

start=Archive_Scraper()
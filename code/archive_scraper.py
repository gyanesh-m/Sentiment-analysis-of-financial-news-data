from bs4 import BeautifulSoup
import requests
import datetime
import lxml
import os
import time
from lxml import html
import pandas as pd
import re
import logging
logging.basicConfig(
    filename="archive.log",
    level=logging.WARNING,
    format="%(asctime)s:%(levelname)s:%(lineno)d:%(message)s"
    )

'''
	 the starting and ending dates are inclusive
'''
class Archive_Scraper:
	def __init__(self,start_dt,end_dt,path):

		self.sd,self.sm,self.sy=start_dt
		self.ed,self.em,self.ey=end_dt
		self.relist,self.collection=self.getRegex(path)

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
						year_month.extend(self.generate_ym_pair(y,1,self.em,non_zero))
					else:
						year_month.extend(self.generate_ym_pair(y,1,12,non_zero))
		return year_month

	def scrape(self,url):
		r = requests.get(url)
		print(url)
		a,b = url.split('//')
		soup = BeautifulSoup(r.content,"html.parser")
		s = ''
		#ndtv.com
		#print(b)
		if b.startswith('www.ndtv')or b.startswith('ndtv'):
			date_data = soup.findAll('span',{"itemprop":'dateModified'})
			#print(date_data)
			j=2
			for i in date_data:
				s = i.get_text().split(" ")
				s[j] = s[j][:-1]
				s = s[j]+'-'+s[j-1][:3]+'-'+s[j+1]
				print(s)
		elif b.startswith('gadgets') or b.startswith('www.gadgets'):#gadgets.ndtv
			date_data = soup.find_all(class_='dtreviewed')
			for i in date_data:
				s = i.get_text().split('"')[0]
				s = s.split(" ")
				s  = s[0]+"-"+(s[1])[0:3]+"-"+s[2]
				print("date",s)
				#s = datetime.datetime.strptime(s, "%d %B %Y")
		elif b.startswith('auto')or b.startswith('www.auto'):
			date_data = soup.find_all(class_='article__pubdate')
			j=0
			for i in date_data:
				if('|' in i.get_text()):
					j=2
				s = i.get_text().split(" ")
				s[j+1] = s[j+1][:-1]
				s = s[j+1]+'-'+s[j]+'-'+s[j+2]
				print(s)
		else:
			date_data = soup.find_all(class_='dateline') #profit.ndtv
			for i in date_data:
				s = i.get_text().split(':')[1]
				a = s.split(' ')
				s = a[2].split(',')
				s = s[0]+'-'+(a[1])[0:3]+'-'+a[3]
				#s = datetime.datetime.strptime(s, "%d-%B-%Y")
				print("date",s)
		
		return s
	def reuters(self):
		url="http://www.reuters.com/resources/archive/us/{year}{month}{date}.html"
		blacklist=['video','#top']
		#collection=[]
		st_d,ed_d=self.sd,self.ed
		year_month=self.year_m(True)
		try:
			for year,month in year_month:
				print("Scraping for the Year " + str(year)," Month " +str(month))
				if(int(month)!=self.sm or int(year)!=self.sy):
					st_d=1
				if(int(month)!=self.em and int(year)!=self.ey):
					ed_d=31
				else:
					ed_d=self.ed
				for d in range(st_d,ed_d+1):
					if(d<10):
						d="0"+str(d)
					r=requests.get(url.format(year=year,month=month,date=d))
					print(r.url)
					if(r.status_code==200):
						b=BeautifulSoup(r.content,'html.parser')
						links=b.select('div > div > div > div > div > div > a')
						print(len(links))
						for link in links:
							try:
								if(not ([i for i in blacklist if link.get('href').find(i)!=-1])):
									for keyword in self.relist:
										if(self.search_key(link.get('href').lower(),self.relist[keyword])):
											index=link.get('href').rfind('/')
											linked="http://www.reuters.com/article"+link.get('href')[index:]
											#print(linked)
											date_object=datetime.date(int(year),int(month),int(d))
											date_,month_,year_=date_object.strftime("%d-%b-%Y").split('-')
											now_d=date_+"-"+month_+"-"+year_
											print(now_d,linked)
											self.collection[keyword].append(now_d+"::"+linked)
							except Exception as e:
								print("#"*10)
								logging.warning(str(link))
								print("#"*10)
					else:
						print("#"*10)
						logging.error(str(r.url))
						print("#"*10)
		except Exception as e:
			print("#"*10)
			logging.critical(e)
			print("#"*10)
		finally:
				#print("Collected "+str(len(self.collection.items()))+" urls for "+self.keyword)
				self.collected()
				self.writeToFile(self.collection,"reutersArchive",self.sd,self.sm,self.sy)

	def econ_times(self):
		base_url="http://economictimes.indiatimes.com/archivelist/year-{year},month-{month},starttime-{start_t}.cms"
		start_time=36892
		start_date=datetime.date(self.sy,self.sm,self.sd)
		days=(start_date-datetime.date(2001,1,1)).days + start_time
		count_days=(datetime.date(self.ey,self.em,self.ed)-start_date).days+1
		
		visit_url=''
		try:
			for day in range(count_days):
				date_diff=datetime.timedelta(day)
				final_date=date_diff+start_date
				print (final_date),
				visit_url=base_url.format(year=final_date.year,month=final_date.month,start_t=days+day)
				try:
					page=requests.get(visit_url)
					print(visit_url)
					xtree=html.fromstring(page.content)
					links=xtree.xpath("*//section[@id='pageContent']//li/a/@href")
					for link in links:
						try:
							for keyword in self.relist:
								if(self.search_key(link.lower(),self.relist[keyword])):
									linked='http://economictimes.indiatimes.com'+link
									date_,month_,year_=final_date.strftime("%d-%b-%Y").split('-')
									now_d=date_+"-"+month_+"-"+year_
									print(now_d,linked)
									self.collection[keyword].append(now_d+"::"+linked)
						except Exception as e:
							print("#"*10)
							logging.warning(str(link))
							print("#"*10)
				except Exception as e:
					print("#"*10)
					logging.error(visit_url)
					print("#"*10)
								
								
		except Exception as e:
			print("#"*10)
			logging.critical(e)
			print("#"*10)
		finally:
			self.collected()
			self.writeToFile(self.collection,"econtimesArchive",self.sd,self.sm,self.sy)

	def thehindu(self):
		base_url="http://www.thehindu.com/archive/web/{year}/{month}/{day}/"
		year_month=self.year_m(True)
		start_date=datetime.date(self.sy,self.sm,self.sd)
		count_days=(datetime.date(self.ey,self.em,self.ed)-start_date).days+1
		#collection=[]
		try:
			for d in range(count_days):
				date_diff=datetime.timedelta(d)
				final_date=date_diff+start_date
				print (final_date),
				visit_url=base_url.format(year=final_date.year,month=final_date.month,day=final_date.day)
				# this webpage loads very slow and becomes unresponsive sometimes hence a timeout of None
				try:
					page=requests.get(visit_url,timeout=None)
					print(visit_url)
					xtree=html.fromstring(page.content)
					links=xtree.xpath("*//ul[@class='archive-list']//a/@href")
					print (len(links))
					for link in links:
						try:
							for keyword in self.relist:
								if(self.search_key(link.lower(),self.relist[keyword])):
									#print(link)
									date_,month_,year_=final_date.strftime("%d-%b-%Y").split('-')
									now_d=date_+"-"+month_+"-"+year_
									print(now_d,link)
									self.collection[keyword].append(now_d+"::"+link)
						except Exception as e:
							print("#"*10)
							logging.warning(str(link))
							print("#"*10)						
				except Exception as e:
					print("#"*10)
					logging.error(visit_url)
					print("#"*10)
		except Exception as e:
			print("#"*10)
			logging.critical(e)
			print("#"*10)
		finally:
			self.collected()
			self.writeToFile(self.collection,"thehinduArchive",self.sd,self.sm,self.sy)

	def ndtv(self):
		base_url="http://archives.ndtv.com/articles/{year}-{month}.html"
		year_month=self.year_m(True)
		start_date=datetime.date(self.sy,self.sm,self.sd)
		end_date = datetime.date(self.ey,self.em,self.ed)
				
		try:
			for d in range(start_date.year-int(self.ey) +1):
				print("Scraping for the year",start_date.year-d)
				try:
					for x in range(start_date.month,end_date.month+1):
						visit_url=base_url.format(year=start_date.year-d,month=str(x).zfill(2))
						page=requests.get(visit_url,timeout=None)
						print(visit_url)
						xtree=html.fromstring(page.content)
						
						links=xtree.xpath("//*[@id='main-content']/ul/li/a/@href")
						print(len(links))
						try:
							for link in links:
								if 'khabar.ndtv' in link or 'hi.ndtv' in link or 'hi.gadgets' in link or 'gadgets.ndtv' in link or 'movies.ndtv' in link or 'food.ndtv' in link:
									continue

								for keyword in self.relist:
									if(self.search_key(link.lower(),self.relist[keyword])):
										self.collection[keyword].append(self.scrape(link)+'::'+link)
						except Exception as e:
							print("#"*10)
							logging.warning(str(link))
							print("#"*10)
							
				except Exception as e:
					print("#"*10)
					logging.error(str(visit_url))
					print("#"*10)
		except Exception as e:
			print("#"*10)
			logging.critical(e)
			print("#"*10)
		finally:
				self.collected()
				self.writeToFile(self.collection,"ndtvArchive",self.sd,self.sm,self.sy)

		

	def businessLine(self):
		base_url="http://www.thehindubusinessline.com/today/?date={date}"
		year_month=self.year_m(True)
		start_date=datetime.date(self.sy,self.sm,self.sd)
		end_date = datetime.date(self.sy,self.em,self.ed)
		print(start_date)
		print(end_date.year)
		try:	
			for i in range(start_date.year-int(self.ey)+1):
				start_date=datetime.date(self.sy-i,self.sm,self.sd)
				end_date = datetime.date(self.sy-i,self.em,self.ed)
				daterange = pd.date_range(start_date, end_date)
				for d in daterange:
						try:
							d  = str(d).split(' ')[0]
							visit_url=base_url.format(date=d)
							page=requests.get(visit_url,timeout=None)
							print(visit_url)
							xtree=html.fromstring(page.content)
							
							links=xtree.xpath("//*[@id='printhide']//a/@href")
							print(len(links))
							for link in links:
								try:
									for keyword in self.relist:
										if(self.search_key(link.lower(),self.relist[keyword])):
											dt=str(datetime.datetime.strptime(d,'%Y-%m-%d').strftime('%d-%b-%Y'))
											print(dt,link)
											self.collection[keyword].append(dt+"::"+link)
								except Exception as e:
									print("#"*10)
									logging.warning(str(link))
									print("#"*10)
							
						except Exception as e:
							print("#"*10)
							logging.error(visit_url)
							print("#"*10)
		except Exception as e:
			print("#"*10)
			logging.critical(e)
			print("#"*10)
		finally:
			self.collected()
			self.writeToFile(self.collection,"businessLineArchive",self.sd,self.sm,self.sy)
#change for others also for write to file definition
	def writeToFile(self,links,webp,date,month,year):
		BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data')
		for company in links:
			try:
				os.makedirs(os.path.join(BASE_PATH,"links",company,'archive'))
			except Exception as e:
				pass
			
			f = open(os.path.join(BASE_PATH,"links",company,"archive","results_"+webp+"_"+company+"_"+str(date)+"_"+str(month)+"_"+str(year)+'.data'),'a+')
			for i in links[company]:
				f.write(str(i)+"\n")
			f.close()

	def search_key(self,input_string,exp):
		exprs=re.compile(exp)

		if(exprs.search(input_string)!=None):
			return True
		else:
			return False
	def getRegex(self,path):
		relist={}
		collection={}
		with open(os.path.join(path),'r+') as fi:
			for line in fi:
				try:
					temp=line.split("::")
					relist[temp[0]]=temp[1].split("\n")[0]
					collection[temp[0]]=[]
				except Exception as e:
					print(e)
					print(line)
		return relist,collection
	def collected(self):
		count={}
		total=0
		for i in self.collection:
			count[i]=len(self.collection[i])
			total+=count[i]
		for i in count:
			print(i+" Collected -"+str(count[i]))
		print("Total Urls collected-"+str(total))


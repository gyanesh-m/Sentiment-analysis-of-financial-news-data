import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import _pickle as pickle
import logging


def tracker(filename):
	f = open("links/tracker.data",'a+')
	for i in f:
		print(i)
		if str(i) != filename:
			f.write(filename+"\n")
	f.close()

def tracked():
	return [line.rstrip('\n') for line in open('links/tracker.data')]
	
def list_files(path):
    # returns a list of names (with extension, without full path) of all files 
    # in folder path
    # excludes temporary files also.
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)) and name.find('tracker.data')==-1 and name.find('empty.txt')==-1 and name not in tracked() and name.find('~')==-1:
            files.append(name)
        else:
        	print("Skipping ",name)
    return files

def make_directory(company,path=None):
	try:
		if path == None:
			os.makedirs('content/'+company)
		else:
			os.makedirs('content/'+company+'/'+path)
	except Exception as e:
		pass	

#All the content scrapers will return a list of strings for a specific website.
def sc_reuters(bs):
	d=bs.find_all(id='article-text')
	content=[i.get_text() for i in d]
	try:
		n=content[-1].rfind("(")
		content[-1]=content[-1][:n]
	except Exception as e:
		print(e)
#	print (content)
	return content

def sc_thehindu(bs):
	temp=bs.select('div > p')
	content=[j.get_text() for i,j in enumerate(temp) if i<len(temp)-3]
	return content

def sc_econt(bs):
	t=[]
	data=bs.find_all(class_='Normal')
	t.append([i.get_text() for i in data])
	return t

def moneyControl(bs):
	t = []
	try:
		temp = []
		data = bs.find_all(class_=['arti-flow','arti-box','arti-flow clearfix'])
		# logging.info(data)
		for i in data:
			temp = temp + (i.find_all('p',text=True))
		for i in temp:
			# logging.info(i.get_text())
			t.append(i.get_text())
	except Exception as e:
		print(e)
	return t
	
def ndtv(bs):
	t=[]
	#profit.ndtv not working :S
	data = bs.find_all(class_=['ins_storybody','content_text row description','fullstoryCtrl_fulldetails'])
	#print(len(data))
	y = []
	for i in data:
		y = y + i.find_all('p',text=True)
	for i in y:
		t.append(i.get_text())
	data = bs.findAll('span',{"itemprop":'articleBody'})
	if len(data) > 0:
		for i in data:
			t.append(i.get_text())
	data = bs.findAll('div',{"itemprop":'articleBody'})
	
	if len(data) > 0:
		for i in data:
			t.append(i.get_text())
	return t
def hindu_bl(bs):
	t=[]
	data = bs.findAll('p',{"class":'body'})
	#data=bs.find_all(class_='article-text')
	# for i in data:
	# 	y=i.find_all('p')
	
	for i in data:
		t.append(i.get_text())
	
	return t

if __name__ == '__main__':
	
	NEWS={'reuters.com':sc_reuters,'thehindu.com':sc_thehindu,'economictimes.indiatimes':sc_econt,'moneycontrol.com':moneyControl,'ndtv.com':ndtv,'hindubusinessline.com':hindu_bl}
	for file in list_files('links/finallinks'):
		links = [line.rstrip('\n') for line in open('links/finallinks/'+file)]
		collection={}
		for k in NEWS:
			collection[k]=[]
		for link in links:
			for key in NEWS:
				if key in link:
					collection[key].append(link)
		company = file.split('_')[1]
		for webp in collection:
			print(webp)
			b = {}
			date = []
			content = []
			_link = []
			for url in collection[webp]:
				c,d= url.split('::')
				# if 'khabar.ndtv' in d:
				# 	continue
				r = requests.get(d)
				print("Scraping url ",d)
				soup = BeautifulSoup(r.content,"html.parser")
				a=NEWS[webp](soup)
				str1=''
				tokens=[]
				for text in a:
					tokens.extend(text)

				for tk in tokens:
					str1+=''.join(tk)
				c = datetime.datetime.strptime(c, '%d-%b-%Y')
				date.append(c)
				content.append(str1)
				_link.append(d)
				temp = {c:str1}
				b.update(temp)
			make_directory(company,webp)
			
			with open('content/'+company+'/'+webp+'/raw_'+file.split('.data')[0]+'_'+webp+'.pkl', 'wb') as fp:
			    pickle.dump(b, fp)
			temp = {'date':date,
					'data':content,
					'url':_link}
			df = pd.DataFrame(temp)
			df.set_index('date',inplace=True)
			df.to_pickle('content/'+company+'/'+webp+'/'+file.split('.data')[0]+'_'+webp+'_content.pkl')
			df.to_csv('content/'+company+'/'+webp+'/'+file.split('.data')[0]+'_'+webp+'_content.csv')
		tracker(file)
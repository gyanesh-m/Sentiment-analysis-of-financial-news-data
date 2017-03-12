import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import _pickle as pickle


def tracker(filename):
	f = open("links/tracker.data",'a+')
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

def make_directory(company):
	try:
		os.makedirs('content/'+company)
	except Exception as e:
		pass	
def sc_reuters(bs):
	data=[]
	d=bs.find_all(id='article-text')
	content=[i.get_text() for i in d]
	n=content[-1].rfind("(")
	content[-1]=content[-1][:n]
	data.extend(content)
	return data

def sc_thehindu(bs):
	t=[]
	temp=bs.select('div > p')
	temp2=[j.get_text() for i,j in enumerate(temp) if i<len(temp)-3]
	t.extend(temp2)
	return t

def sc_econt(bs):
	t=[]
	data=bs.find_all(class_='Normal')
	t.append([i.get_text() for i in data])
	return t

def moneyControl(bs):
	t = []
	try:
		data = bs.find_all(class_=['arti-flow','arti-box'])
		temp = []
		for i in data:
			temp = i.find_all('p')
		for i in temp:
			t.append(i.get_text())

	return t

def ndtv(bs):
	t=[]
	#profit.ndtv not working :S
	data = bs.find_all(class_=['ins_storybody','content_text row description','fullstoryCtrl_fulldetails'])
	print(len(data))
	y = []
	for i in data:
		y = i.find_all('p')
	for i in y:
		t.append(i.get_text())
	return t

NEWS={'reuters.com':sc_reuters,'thehindu.com':sc_thehindu,'economictimes.indiatimes':sc_econt,'moneycontrol.com':moneyControl,'ndtv.com':ndtv}
for file in list_files('links/'):
	print(file)
	company = file.split('_')[2]
	links = [line.rstrip('\n') for line in open('links/'+file)]
	webp=file.split('_')[1]
	print(webp)
	b = {}
	date = []
	content = []
	for url in links:
		c,d= url.split('::')
		if 'khabar.ndtv' in d:
			continue
		r = requests.get(d)
		print("Scraping url ",d)
		soup = BeautifulSoup(r.content,"html.parser")

		a=NEWS[webp](soup)

		str1 = ''.join(a)
		c = datetime.datetime.strptime(c, '%d-%b-%Y')
		date.append(c)
		content.append(str1)
		temp = {c:str1}
		b.update(temp)

	make_directory(company)

	with open('content/'+company+'/raw_'+file.split('.data')[0]+'.pkl', 'wb') as fp:
	    pickle.dump(b, fp)

	temp = {'date':date,
			'data':content}

	df = pd.DataFrame(temp)
	df.set_index('date',inplace=True)
	df.to_pickle('content/'+company+'/'+file.split('.data')[0]+'_content.pkl')
	df.to_csv('content/'+company+'/'+file.split('.data')[0]+'_content.csv')
	tracker(file)
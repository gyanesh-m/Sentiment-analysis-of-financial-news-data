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
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)) and name != 'tracker.data' and name not in tracked():
            files.append(name)
        else:
        	print("Skipping ",name)
    return files

def make_directory(company):
	try:
		os.makedirs('content/'+company)
	except Exception as e:
		pass	

for file in list_files('links/'):
	company = file.split('_')[1]
	links = [line.rstrip('\n') for line in open('links/'+file)]
	
	b = {}
	date = []
	content = []
	for url in links:
		c,d= url.split('::')
		r = requests.get(d)
		print("Scraping url ",d)
		soup = BeautifulSoup(r.content,"html.parser")

		link = soup.find_all("p")
		#head = soup.find_all('h1')
		a = []
		# for x in head:
		# 	a.append(x.text)

		for data in link:
			a.append(data.text);

		str1 = ''.join(a)
		c = datetime.datetime.strptime(c, '%d-%b-%Y')
		date.append(c)
		content.append(str1)
		temp = {c:str1}
		#print(url)
		b.update(temp)
		# with open('scraped_data.data', 'w', encoding='utf-8') as f:
		#     print(b, file=f)

	# import json
	# with open('content/result_'+file.split('data')[0]+'.json', 'w') as fp:
	#     json.dump(b, fp,indent=4)
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
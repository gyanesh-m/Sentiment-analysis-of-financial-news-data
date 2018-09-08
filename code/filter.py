import requests
import os
from bs4 import BeautifulSoup
from scrape_with_bs4 import sc_reuters,sc_econt,sc_thehindu,moneyControl,ndtv,hindu_bl
from nltk.tokenize import sent_tokenize
# checks for the presence of a word in a string by checking character before 
#the start of the word and after the end of the word
NEWS={
		'reuters.com':sc_reuters,
		'thehindu.com':sc_thehindu,
		'economictimes.indiatimes':sc_econt,
		'moneycontrol.com':moneyControl,
		'ndtv.com':ndtv,
		'thehindubusinessline.com':hindu_bl
	}
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

class Filter(object):
	def __init__(self):
		pass
	def search_key(self,input_string,word):
			index=input_string.find(word)
			if(index!=-1):
				if(index!=0):
					low=ord(input_string[index-1])
				else:
					low=95
				if(index+len(word)!=len(input_string)):
					high=ord(input_string[index+len(word)])
				else:
					high=95
				if( (low<97 or low>122) and ( high<97 or high>122) ):
					return True
				else:
					return search_key(input_string[index+len(word):],word)
			else:
				return False

	def main(self):
		os.chdir(os.path.join(BASE_PATH,'..','data','links'))
		print("Enter company name to filter results for among ")
		print([ i for i in os.listdir() if 'empty.txt' not in i])
		company=input()
		print("Chose option regarding file name:\n ",
				"1. Keep old file and new name is old name appended with _\n",
				" 2. Overwrite old file\n")
		name_change=input()
		if name_change=='1':
			name_change='_'
		else:name_change=''
		print(name_change)
		for path, subdirs, files in os.walk(os.path.join(BASE_PATH,'links',company)):
				#avoids archive subdir and its path
				if(path.rfind('archive')==-1 and len(files)!=0):
					print(files)
					for file in files:
						filtered_links=[]
						print("Filtering for "+file)
						with open(path+'/'+file, 'r') as in_file:
							links = [line.rstrip('\n') for line in in_file]
						for key in NEWS:
							if key in file:
								for url in links:
									try:
										print(url)
										#checks for the inurl presence of the company name
										if(search_key(url.lower(),company.lower())):
											filtered_links.append(url)
											print("*"*8+"Passed")
											continue
										count=0
										r = requests.get(url.split('::')[1])
										soup = BeautifulSoup(r.content,"html.parser")			
										#extracts content from the respective scraper
										list_of_sentences=NEWS[key](soup)	
										tokens=[]
										for x in list_of_sentences:
											tokens.extend(sent_tokenize(str(x)))
										for tk in tokens:
											if(search_key(tk.lower(),company)):
												count+=1
										if(count>=2):
											filtered_links.append(url)
											print("count-"+str(count))
									except Exception as e:
										print(e)
						wfile=open(path+'/'+file+name_change,'w+')
						for lnk in filtered_links:
							wfile.write(lnk)
							wfile.write('\n')
						wfile.seek(0,0)
						print('#'*12)
						print("##written "+str(len(filtered_links)))
						wfile.close()
						print("##original "+str(len(links)))
						print('#'*12)
filter_it = Filter()
filter_it.main()


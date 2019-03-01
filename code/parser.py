import json
import argparse
import os
from archive_scraper import *
from merger import *

BASE_DIR = os.path.join(os.getcwd(),'..')

def parse():
	parser = argparse.ArgumentParser(description="Runs the entire pipeline from scraping to extracting sentiments.",
									 formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument('-s','--start',type=str,help="Start date,format-(dd/mm/yy)\n",required=True)
	parser.add_argument('-e','--end',type=str,help="End date,format-(dd/mm/yy)",required = True)
	parser.add_argument('-w','--web',type=int,nargs='*',required = True, help="Specify the website number to scrape from separated by space\
						\n0=economictimes.indiatimes.com\
						\n1=reuters.com\
						\n2=ndtv.com\
						\n3=thehindubusinessline.com\
						\n4=moneycontrol.com\
						\n5=thehindu.com")
	parser.add_argument('-r','--regexp',type=str,help="Complete path to the regex list file for companies. \nFor template refer regesList file at root directory of this repo.\n By default, it runs the regexList file present at root directory of this repo.",default=os.path.join(BASE_DIR,'regexList'))
	# parser.add_argument('-m','--mode',type=int,help="Which operation to perform.")
	args = parser.parse_args()
	s=args.start
	e=args.end
	w=args.web
	reg = args.regexp
	s=map(int,s.split('/'))
	e=map(int,e.split('/'))
	print(s,e)
	## using archive scraper to get the news url
	archive_sc = Archive_Scraper(s,e,reg)
	for option in w:
		if(option==0):
			print("Scraping from Economictimes")
			archive_sc.econ_times()
		elif(option==1):
			print("Scraping from reuters")
			archive_sc.reuters()
		elif(option==2):
			print("Scraping from NDTV Yolo")
			archive_sc.ndtv()
		elif(option==3):
			print("Scraping BusinessLine")
			archive_sc.businessLine()
		elif(option==4):
			print("Scraping from thehindu")
			archive_sc.thehindu()
	## using merger to merge different versions of archive runs and also remove duplicates
	print("merger")
	entity_names = archive_sc.collection.keys()
	merge = Merger(entity_names)

	## running scrapy
	#	todo

	## Finding sentiment
	# 	todo

if __name__ == '__main__':
	parse()
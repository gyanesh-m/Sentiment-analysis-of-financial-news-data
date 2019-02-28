import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import os
import _pickle as pickle
import logging

#All the content scrapers will return a list of strings for a specific website.
class ContentScrape:
	def __init__(self):
		pass

	def reuters(self,bs):
		d = bs.find_all("div",{"class":"StandardArticleBody_body"})
		content=[i.get_text() for i in d]
		return content

	def thehindu(self,bs):
		temp=bs.select('div > p')
		content=[j.get_text() for i,j in enumerate(temp) if i<len(temp)-3]
		return content

	def econt(self,bs):
		t=[]
		data=bs.find_all(class_='Normal')
		t.append([i.get_text() for i in data])
		return t

	def moneyControl(self,bs):
		t = []
		try:
			temp = []
			data = bs.find_all(class_=['arti-flow','arti-box','arti-flow clearfix'])
			for i in data:
				temp = temp + (i.find_all('p',text=True))
			for i in temp:
				t.append(i.get_text())
		except Exception as e:
			print(e)
		return t
		
	def ndtv(self,bs):
		t=[]
		#profit.ndtv not working :S
		data = bs.find_all(class_=['ins_storybody','content_text row description','fullstoryCtrl_fulldetails'])
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
	def hindu_bl(self,bs):
		t=[]
		data = bs.findAll('p',{"class":'body'})
		for i in data:
			t.append(i.get_text())
		
		return t

class TitleScrape:
	def __init__(self):
		pass

	def reuters(self,bs):
		t = []
		data = bs.findAll('h1',{"class":'ArticleHeader_headline'})
		if len(data) > 0:
			for i in data:
				print(i.get_text())
				t.append(i.get_text())
		return t

	def thehindu(self,bs):
		t = []
		data = bs.findAll('h1',{"class":'title'})
		if len(data) > 0:
			for i in data:
				# print(i.get_text())
				t.append(i.get_text())
		return t

	def econt(self,bs):
		t=[]
		data=bs.select('body > section.pageHolder > div.clearfix.relative > div.article_wrap.flt > div > section > div.relative > article > h1')
		t.append([i.get_text() for i in data])
		# print(t)
		return t

	def moneyControl(self,bs):
		t = []
		try:
			temp = []
			data = bs.find_all(class_=['h1'])
			logging.info(data)
			# for i in data:
			# 	temp = temp + (i.find_all('p',text=True))
			for i in temp:
				print(i.get_text())
				t.append(i.get_text())
		except Exception as e:
			print(e)
		return t
		
	def ndtv(self,bs):
		t=[]
		#profit.ndtv not working :S
		data = bs.findAll('h1',{"itemprop":'headline'})
		if len(data) > 0:
			for i in data:
				# print(i.get_text())
				t.append(i.get_text())
		return t
	def hindu_bl(self,bs):
		t=[]
		data = bs.findAll('h1',{"class":'detail-title'})
		for i in data:
			# print(i.get_text())
			t.append(i.get_text())
		
		return t

def tracker(filename,path):
	f = open(os.path.join(path,"links/tracker.data"),'a+')
	for i in f:
		print(i)
		if str(i) != filename:
			f.write(filename+"\n")
	f.close()

def tracked(path):
	if(os.path.isfile(os.path.join(path,'..','tracker.data'))):
		return [line.rstrip('\n') for line in open(os.path.join(path,'..','..','tracker.data'))]
	print(os.path.join(path,'..','..','tracker.data'))
	return []

def list_files(path):
    # returns a list of names (with extension, without full path) of all files 
    # in folder path
    # excludes temporary files also.
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)) and name.find('tracker.data')==-1 and name.find('empty.txt')==-1 and name not in tracked(path) and name.find('~')==-1:
            files.append(name)
        else:
        	print("Skipping ",name)
    return files
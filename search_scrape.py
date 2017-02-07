from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import selenium 
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
import random
print("")
print("#"*8+" Enter the details to scrape separated by SPACE.")
sd,sm,sy=raw_input("Enter starting day month year ").split(" ")
ed,em,ey=raw_input("Enter ending day month year ").split(" ")
webp=raw_input("Enter website to scrape- ")
comp=raw_input("Enter company data to scrape -")
driver = webdriver.Chrome(executable_path="/home/zoro/beautiful_soup/chromedriver")
driver.implicitly_wait(15)
start_url="https://www.google.co.in/search?num=100&biw=1040&bih=635&tbs=cdr%3A1%2Ccd_min%3A"+"{smonth}"+r"%2F"+"{sday}"+r"%2F"+"{syear}"+r"%2Ccd_max%3A"+"{emonth}"+r"%2F"+"{eday}"+r"%2F"+"{eyear}"+r"%2Csbd%3A1&tbm=nws&q=site%3A"+"{webpage}+%22{company}%22&&oq=site%3A{webpage}"+"%22{company}%22&gs_l=serp.3...0.0.0.1565.0.0.0.0.0.0.0.0..0.0....0...1c..64.serp..0.0.0.IfKqhHBbtbY"
driver.get(start_url.format(smonth=sm,sday=sd,syear=sy,emonth=em,eday=ed,eyear=ey,webpage=webp,company=comp))
data={}
next_page=""
wait = WebDriverWait(driver, 15)
i=0
time.sleep(10)
previous=next_page
while next_page is not None or previous is not None:
		time.sleep(random.randrange(15,20))
		list_links=[]
		try:
			next_page = wait.until(EC.element_to_be_clickable((By.ID,'navcnt')))
			next_page = driver.find_element_by_link_text('Next')
			element=driver.find_elements_by_xpath("*//h3/a")
		except Exception as e:
			print (e)
			next_page=None
			#this is for the last page when no next option will be available
			element=driver.find_elements_by_xpath("*//h3/a")
		for ele in element:
			list_links.append(ele.get_attribute("href"))
		data[i]=list_links
		print (list_links)
		i+=1
		if next_page is not None:
			next_page.click()
		else:
			break
print("*"*8+"Finished fetching all the urls"+"*"*8)
count=0
for i in data.keys():
	count+=len(data[i])
print("#"*8+"Fetched "+str(count))

data_file=open("gresults_"+comp+" "+sd+":"+sm+":"+sy+'w+')
data_file.write("#"*8+"Fetched "+str(count))
for i in range(len(data)):
	data_file.write(str(i)+":"+str(data[i]))
	data_file.write("\n")
data_file.close()
#driver.close()
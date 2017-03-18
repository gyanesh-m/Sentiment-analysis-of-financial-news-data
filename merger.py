import os
from difflib import SequenceMatcher
def data_generator(company,option,webs=None,base_path=None):
			links=[]
			if(webs!=None):
				for web in webs:
					os.chdir(os.path.join(base_path,web))
					years=[year for year in os.listdir() if year and os.path.isdir(year)]
					for year in years:
						os.chdir(os.path.join(base_path,web,year))
						files=[afile for afile in os.listdir() if afile and not os.path.isdir(afile)]
						for data_file in files:
							with open(data_file,'r') as ff:
								for line in ff:
									x,y=line.split("::")
									links.append((x,y))
			os.chdir(os.path.join(base_path))
			files_=[i for i in os.listdir() if i not in ignore and not os.path.isdir(i)]
			for f_name in files_:
				with open(f_name,'r')as ff:
					for line in ff:
							x,y=line.split("::")
							links.append((x,y))
				if(option==1 and f_name!='results_'+company):
					os.rename(f_name,'raw_links/'+f_name)
			return links
def sequence_matcher(opt,comp,links_g=None,webs=None,path=None):
		if(opt==2):
			links=data_generator(webs=webs,option=opt,base_path=path,company=comp)
			links.extend(data_generator(option=opt,base_path=os.path.join(path,'archive'),company=comp))
		elif (opt==1):
			links=data_generator(option=opt,base_path=path,company=comp)
		stats={0.2:0,0.4:0,0.6:0,0.8:0,1:0}
		regret=[]		
		count=0
		print(len(links))
		for i in links:		
				count+=1
				print(count,len(links))
				seq=SequenceMatcher(None,i[1],'')
				for j in links:
					if(i!=j):
						seq.set_seq2(j[1])
						value=seq.ratio()
						if(value<=0.2):
							stats[0.2]+=1
						elif(value<=0.4):
							stats[0.4]+=1
						elif(value<=0.6):
							stats[0.6]+=1
						elif(value<=0.8):
							stats[0.8]+=1
						elif(value>=0.85):
							stats[1]+=1
							links.remove(j)
							regret.append(j)
		if(option==1):
			os.chdir(path)
		else:
			os.chdir(BASE_PATH)
		print(path)
		f_name='results_'+comp+'.data'
		with open(f_name,'a+') as f:
			for i in links:
				f.write(str(i[0])+"::"+str(i[1]))
		print("Stats for this file\n\nSimilarity Score(<=) \t occurances")
		for i in stats:
			print ('\t'+str(i)+'\t\t\t'+str(stats[i]))
		print("final count "+str(count)+" urls\n\n" )
		print("removed "+str(len(regret))+" urls")
		print(regret)


ignore=['empty.txt','tracker.data']	
os.chdir('links')
companies=[i for i in os.listdir() if i not in ignore and os.path.isdir(i)]
BASE_PATH=os.getcwd()
option=int(input("Select the operation to perform for all existing companies\n 1. Remove duplicate entries from the archives\n 2. Merge archive and google results\n"))
print (companies)
for i in companies:
		if(option==1):
			os.chdir(os.path.join(BASE_PATH,i+'/archive'))
			print ("Removing duplicates for "+i)
			files=[afile for afile in os.listdir() if afile not in ignore and not os.path.isdir(afile)]
			try:
				os.mkdir('raw_links')
			except:
				pass
			sequence_matcher(path=os.getcwd(),opt=option,comp=i)				
		elif(option==2):
			os.chdir(os.path.join(BASE_PATH,i))
			websites=[web for web in os.listdir() if web not in ignore and os.path.isdir(web) and web!="archive"]			
			print(websites)
			temp_path=os.path.join(BASE_PATH,i)
			sequence_matcher(webs=websites,path=temp_path,opt=option,comp=i)
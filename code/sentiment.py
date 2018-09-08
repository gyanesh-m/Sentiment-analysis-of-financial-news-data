from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import pandas as pd
import numpy as np
import os

BASE_PATH = os.path.join(os.getcwd(),'..','data')

sid = SentimentIntensityAnalyzer()

def analyze(file):
    df = pd.read_csv(file)
    sent = {}
    pos = []
    neg = []
    com = []
    neu = []
    print(len(df))
    i = 0
    for date, data in df.iterrows():
        i+=1
        sent[i] = sid.polarity_scores(str(data['data']))
        pos.append(sent[i]['pos'])
        neg.append(sent[i]['neg'])
        neu.append(sent[i]['neu'])
        com.append(sent[i]['compound'])

    df['positive'] = pos
    df['negative'] = neg
    df['neutral'] = neu
    df['compound'] = com

    df.to_csv(file.split('.csv')[0]+'_sentiment'+'.csv')
    #print(df.head())

if __name__ == '__main__':
    list_files = os.listdir(os.path.join(BASE_PATH,'content'))
    print("Select the folder number to generate sentiment for.")
    for i,j in enumerate(list_files):
        print(str(i)+' - ' + j)
    file_number = input()
    for path, subdirs, files in os.walk(os.path.join(BASE_PATH,'content',list_files[file_number])):
        for f in files:
            if f.endswith('.csv'):
                f = os.path.join(BASE_PATH,'content',i,f.split('_')[3],f)
                print(f)
                analyze(f)



from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import pandas as pd
import numpy as np
import os

BASE_PATH = os.path.join(os.getcwd(),'..','data')

sid = SentimentIntensityAnalyzer()

def analyze(file):
    df = pd.read_csv(file)
    cols = list(df.columns)
    for col in cols:
        if 'content' in cols:
            pref = 'content'
            cols.remove('content')
        elif 'title' in cols:
            pref = 'title'
            cols.remove('title')
        else:
            continue
        sent = {}
        pos = []
        neg = []
        com = []
        neu = []
        print(len(df))
        i = 0
        for date, data in df.iterrows():
            i+=1
            sent[i] = sid.polarity_scores(str(data[pref]))
            pos.append(sent[i]['pos'])
            neg.append(sent[i]['neg'])
            neu.append(sent[i]['neu'])
            com.append(sent[i]['compound'])

        df[pref+'_positive'] = pos
        df[pref+'_negative'] = neg
        df[pref+'_neutral'] = neu
        df[pref+'_compound'] = com

    df.to_csv(file.split('.csv')[0]+'_sentiment'+'.csv')

if __name__ == '__main__':
    list_files = os.listdir(os.path.join(BASE_PATH,'content'))
    print("Select the folder number to generate sentiment for.")
    for i,j in enumerate(list_files):
        print(str(i)+' - ' + j)
    file_number = int(input())
    for path, subdirs, files in os.walk(os.path.join(BASE_PATH,'content',list_files[file_number])):
        for f in files:
            if f.endswith('.csv'):
                print(BASE_PATH,'content',list_files[file_number],f.split('_')[3],f)
                f = os.path.join(BASE_PATH,'content',list_files[file_number],f.split('_')[3],f)
                print(f)
                analyze(f)
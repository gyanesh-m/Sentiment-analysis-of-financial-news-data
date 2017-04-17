from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import pandas as pd
import numpy as np
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

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
    i = input("Enter the company\n[hdfc,maruti-suzuki,itc,tcs,sbi,ongc,sun-pharma\n")

    for path, subdirs, files in os.walk(os.path.join(BASE_PATH,'content',i)):
        for f in files:
            if f.endswith('.csv'):
                f = os.path.join(BASE_PATH,'content',i,f.split('_')[3],f)
                print(f)
                analyze(f)



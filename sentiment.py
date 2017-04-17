from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize

# l1 = ["NEW DELHI: India's largest car manufacturer Maruti Suzuki has announced that the Automatic (Continuous Variable Transmission-CVT) will now be available as an option on the Zeta (Petrol) variant of Baleno.",
# "It has been priced at Rs 7,47,701, ex-showroom Delhi.Earlier it was available on the Delta variant only.",
# " Since its launch in October 2016, over 44,000 Baleno cars have been sold through Maruti Suzuki's premium retail channel NEXA across India and in addition there are over 55,000 bookings to be served.Baleno is also the first model by Maruti Suzuki to be exported to Japan.",
# " Going forward Maruti Suzuki plans to export the model to more than 100 countries from India. Introducing the new variant RS Kalsi, Executive Director (Marketing & Sales), Maruti Suzuki India, said,"" Baleno has rapidly found success to become a popular premium hatchback owing to its design, technology and performance. The automatic option - Continuous Variable Transmission - offered on the Delta variant has been much appreciated by the customers.",
# " We are now offering CVT on the Zeta variant as well, to popularise two pedal technologies."]

# l2 = "NEW DELHI: India's largest car manufacturer Maruti Suzuki has announced that the Automatic (Continuous Variable Transmission-CVT) will now be available as an option on the Zeta (Petrol) variant of Baleno. It has been priced at Rs 7,47,701, ex-showroom Delhi.Earlier it was available on the Delta variant only. Since its launch in October 2016, over 44,000 Baleno cars have been sold through Maruti Suzuki's premium retail channel NEXA across India and in addition there are over 55,000 bookings to be served.Baleno is also the first model by Maruti Suzuki to be exported to Japan. Going forward Maruti Suzuki plans to export the model to more than 100 countries from India. Introducing the new variant RS Kalsi, Executive Director (Marketing & Sales), Maruti Suzuki India, said,"" Baleno has rapidly found success to become a popular premium hatchback owing to its design, technology and performance. The automatic option - Continuous Variable Transmission - offered on the Delta variant has been much appreciated by the customers. We are now offering CVT on the Zeta variant as well, to popularise two pedal technologies."
# l =""""

# Italian car maker Fiat FIA.MI said it will supply 100,000 more small diesel engines to Suzuki Motor Corp's (7269.T) Indian unit, in addition to those already licensed, amid strong demand in the Indian car market.
# Fiat will supply up to 100,000 more diesel engines a year for three years to Maruti Suzuki (MRTI.NS), 54.2 percent owned by Suzuki.
# The 1.3L MultiJet 75hp engine will be used in Suzuki cars in India produced by Suzuki's local Indian affiliate Maruti Suzuki India Limited.
# It is the same engine that Fiat supplies to General Motors (GM.N) in Europe, and the same engine that Fiat uses to power its Fiat 500, Fiat Punto and the Fiat Panda."
# """
# l3 = sent_tokenize(l)
# print(len(l3))
# score = {}
# neg = 0
# neu = 0
# pos = 0
# compound = 0
# for i in l:
#     sid = SentimentIntensityAnalyzer()
#     ss = sid.polarity_scores(i)
#     neg = (neg + ss['neg'])/len(l1)
#     neu = (neu + ss['neu'])/len(l1)
#     pos = (pos + ss['pos'])/len(l1)
#     compound = (compound + ss['compound'])/len(l1)

# print("Neg:",neg,"-Neu:",neu,"-Pos:",pos,"-Compound:",compound)

# ss = sid.polarity_scores(l2)
# print(ss)

# ss = sid.polarity_scores(l)
# print(ss)

import pandas as pd
import numpy as np
import os
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

sid = SentimentIntensityAnalyzer()

def analyze(file):
    df = pd.read_csv(file)
    # d = iris.head()['date']
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



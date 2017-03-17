import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
style.use('ggplot')

web_stats = {'Day':[1,2,3,4,5,6],
			'Visitors':[43,35,23,56,78,12],
			'Bounce_rate':[23,45,67,84,57,45]}

df = pd.DataFrame(web_stats)

# print(df.head())
# print(df.tail(2))
# print(df)

df.set_index('Day',inplace = True) #returns a dataframe inplace does df = df.set_index('ind')

# print(df['Visitors'])
print(df.Visitors.tolist()) #same as above
print(np.array(df[['Bounce_rate','Visitors']]))
print(df[['Bounce_rate','Visitors']])
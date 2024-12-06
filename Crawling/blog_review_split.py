import pandas as pd
import numpy as np


file = '/Users/jieunsong/Desktop/git/Hadoop-Classification/data/crawling/Seoul-all_restaurants.CSV'
filename = file.split('.')[0]

df = pd.read_csv(file)

print(df.shape)
print()

print(df.head())
print()

n = 1200
for idx,(_, sub_df) in enumerate(df.groupby(np.arange(len(df)) // n)):
    print('save to csv', sub_df.shape)
    print()
   
    sub_df.to_csv(filename+str(idx) + ".csv", index=False)

    print("-" * 50)  # 구분선
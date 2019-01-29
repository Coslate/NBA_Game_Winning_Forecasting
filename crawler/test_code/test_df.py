#! /usr/bin/env python3.6

import pandas as pd
import numpy as np
np.random.seed(5)
df = pd.DataFrame(np.random.randint(100, size=(100, 6)),
                  columns=list('ABCDEF'),
                  index=['R{}'.format(i) for i in range(100)])

print(df['C'].head().to_string())
a_list = list(df['C'].head().values)
print(a_list)
index_val_larger_50 = [i for (i, x) in enumerate(a_list) if x > 50]
print('--------')
print(index_val_larger_50)
print('--------')
new_df_list = [df.iloc[index] for index in index_val_larger_50]
new_df = pd.DataFrame(data=new_df_list, columns = df.columns, index=df.index[0:len(new_df_list)])
print(new_df.head())
print('--------')
print(df.head())


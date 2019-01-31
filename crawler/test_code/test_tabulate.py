#! /usr/bin/env python3.6
import pandas as pd
import numpy as np
from tabulate import tabulate

df2 = pd.DataFrame(np.random.randint(low=0, high=10, size=(5, 5)),columns=['a', 'b', 'c', 'd', 'e'])
df2_tab = tabulate(df2, headers='keys', tablefmt='psql')
print(f'{type(df2_tab)}')
print('\ndetailed : \n'+df2_tab)

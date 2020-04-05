import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

df = sm.datasets.macrodata.load_pandas().data

print(df.head())

index = pd.Index(sm.tsa.datetools.dates_from_range('1959Q1', '2009Q3'))

df.index = index

print(df.head())

# Tuple unpacking
gdp_cycle, gdp_trend = sm.tsa.filters.hpfilter(df.realgdp)

df["trend"] = gdp_trend

df[['trend','realgdp']]["2000-03-31":].plot(figsize=(12,8))

plt.show()
import quandl as q
import matplotlib.pyplot as plt

hcl_EOD = q.get("BSE/BOM532281", authtoken="NNVwxTvRt_GdzLtj6Zzt", start_date="2019-09-30")

print(hcl_EOD.head())

hcl_EOD['Open'].plot()


plt.show()

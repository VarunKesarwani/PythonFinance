import pandas as pd

df = pd.read_html('https://www.samco.in/knowledge-center/articles/nse-listed-companies/')
print(df[0].head(50))#heads get first 5 records only
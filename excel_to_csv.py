import pandas as pd
import openpyxl

df = pd.read_excel("European Tour - wyniki.xlsx")
df.to_csv("European Tour - wyniki.csv", sep=";", date_format='%d.%m.%Y', index=False)
import pandas as pd


df = pd.read_csv("static/for_query.csv")
print(*[f"(\'{row['NumCode']}\', \'{row['CharCode']}\', \'{row['Name']}\')" for _, row in df.iterrows()], sep=",\n", end=";")
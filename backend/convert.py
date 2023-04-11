import pandas as pd

# df = pd.read_excel("C:\\Users\\angzou\\Downloads\\DOA知识库.xlsx")

df = pd.read_csv("C:\\Users\\angzou\\Downloads\\DOA-v4.csv", sep="|", encoding="utf-8-sig")

df.to_csv("C:\\Users\\angzou\\Downloads\\DOA-v5.csv", index=False, sep="|", encoding="utf-8-sig")

print(df.head(5))
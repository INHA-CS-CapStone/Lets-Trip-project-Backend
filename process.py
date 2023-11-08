import pandas as pd
import sqlite3

df = pd.read_csv("Place.csv", encoding='utf-8-sig')

database = "db.sqlite3"
conn = sqlite3.connect(database)
dtype={
    "name": "CharField",
    "keyword": "CharField",
    "rating": "FloatField", 
    "type": "CharField",
    "review_count": "IntegerField"
}
df.to_sql(name='home_place', con=conn, if_exists='replace', dtype=dtype, index=True, index_label="id")
conn.close()
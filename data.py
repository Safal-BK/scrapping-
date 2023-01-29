import sqlite3
import pandas as pd

con = sqlite3.connect("database/patent_list_db.sqlite")

# Load the data into a DataFrame
data = pd.read_sql_query("SELECT * from patent_list", con)

# # Select only data for 2002
# surveys2002 = surveys_df[surveys_df.year == 2002]

# Write the new DataFrame to a new SQLite table
# patentList_df.to_sql("surveys2002", con, if_exists="replace")



for idx,row in data.iterrows():
    link = row['xml_link']
    print(link)
con.close()
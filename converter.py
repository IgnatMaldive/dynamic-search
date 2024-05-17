import pandas as pd
import sqlite3

# Load CSV data
df = pd.read_csv('data.csv')

# Create SQLite database and save data
conn = sqlite3.connect('data.db')
df.to_sql('data', conn, if_exists='replace', index=False)
conn.close()

print("CSV data has been successfully migrated to SQLite.")

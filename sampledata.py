import pandas as pd
import sqlite3
from datetime import datetime
import io

# Sample data as string
csv_data = """timestamp,steps,heart_rate,sleep_duration
01-01-2026 08:00:00,8500,72,7.5
02-01-2026 08:00:00,9200,75,8.0
03-01-2026 08:00:00,7800,68,6.8
04-01-2026 08:00:00,10500,82,7.2
05-01-2026 08:00:00,8900,70,7.8"""

# Load data into pandas DataFrame
df = pd.read_csv(io.StringIO(csv_data))
df['timestamp'] = pd.to_datetime(df['timestamp'])
print("Loaded data:")
print(df)

# Connect to SQLite database and store data
conn = sqlite3.connect('fitness.db')
df.to_sql('tracker_data', conn, if_exists='replace', index=False)

# Verify: query data
stored_df = pd.read_sql_query("SELECT * FROM tracker_data LIMIT 5;", conn)
print("\nStored in SQLite:")
print(stored_df)
conn.close()
print("\nData stored successfully in fitness.db")

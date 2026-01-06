import pandas as pd
import sqlite3
import io
import time
from concurrent.futures import ThreadPoolExecutor
import random
from threading import Lock

# Your sleep_score function
def sleep_score(duration):
    if 7 <= duration <= 9: return 1.0
    elif 6 <= duration < 7 or 9 < duration <= 10: return 0.7
    else: return 0.3

def process_user_data(user_id):
    """Thread-safe: each thread gets own temp DB"""
    csv_data = f"""timestamp,steps,heart_rate,sleep_duration
2026-01-01 08:00:00,{8500+user_id*100},72,7.5
2026-01-02 08:00:00,{9200+user_id*100},75,8.0
2026-01-03 08:00:00,{7800+user_id*100},68,6.8
2026-01-04 08:00:00,{10500+user_id*100},82,7.2
2026-01-05 08:00:00,{8900+user_id*100},70,7.8"""
    
    df = pd.read_csv(io.StringIO(csv_data))
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['sleep_quality'] = df['sleep_duration'].apply(sleep_score)
    df['user_id'] = user_id
    
    # Thread-local SQLite 
    temp_conn = sqlite3.connect(f'temp_user_{user_id}.db')
    df.to_sql('tracker_data', temp_conn, if_exists='replace', index=False)
    temp_conn.close()
    
    avg_steps = df['steps'].mean()
    return {'user_id': user_id, 'avg_steps': avg_steps, 'sleep_score': df['sleep_quality'].mean(), 'records': len(df)}

# 1. SEQUENTIAL
print("=== SEQUENTIAL ===")
start = time.time()
results_seq = [process_user_data(i) for i in range(1, 5)]
seq_time = time.time() - start
print(f" {seq_time:.2f}s | 5 users")

# 2. CONCURRENT 
print("\n=== THREAD-SAFE MULTITHREADING ===")
start = time.time()
with ThreadPoolExecutor(max_workers=5) as executor:
    results_con = list(executor.map(process_user_data, range(1, 5)))
con_time = time.time() - start
print(f" {con_time:.2f}s | 5 users")

# Merge all temp DBs to master
master_conn = sqlite3.connect('fitness_concurrent.db')
for result in results_con:
    temp_df = pd.read_sql("SELECT * FROM tracker_data", sqlite3.connect(f'temp_user_{result["user_id"]}.db'))
    temp_df.to_sql('all_users', master_conn, if_exists='append', index=False)
master_conn.close()

speedup = seq_time / con_time
print(f"\ {speedup:.1f}x SPEEDUP ({seq_time:.2f}s → {con_time:.2f}s)")
print("Sample results:", results_con[:3])

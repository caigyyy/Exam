import pandas as pd
import matplotlib.pyplot as plt
import io

# Data sample
csv_data = """timestamp,steps,heart_rate,sleep_duration
2026-01-01 08:00:00,8500,72,7.5
2026-01-02 08:00:00,9200,75,8.0
2026-01-03 08:00:00,7800,68,6.8
2026-01-04 08:00:00,10500,82,7.2
2026-01-05 08:00:00,8900,70,7.8"""

df = pd.read_csv(io.StringIO(csv_data))
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Create line graph for daily steps trend
plt.figure(figsize=(10, 6))
plt.plot(df['timestamp'], df['steps'], marker='o', linewidth=2, label='Daily Steps')
plt.axhline(df['steps'].mean(), color='r', linestyle='--', label=f'Average: {df["steps"].mean():.0f}')
plt.title('Daily Steps Trend', fontsize=14)
plt.xlabel('Date')
plt.ylabel('Steps')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('steps_trend.png', dpi=300)
plt.show()  

# Scatter plot for correlation between Heart Rate and Steps
import matplotlib.pyplot as plt
plt.scatter(df['steps'], df['heart_rate'], s=100, c='coral')
plt.xlabel('Steps')
plt.ylabel('Heart Rate (BPM)')
plt.title('Steps vs Heart Rate Correlation')
plt.grid(True, alpha=0.3)
plt.savefig('hr_steps_scatter.png')
plt.show()

# Bar chart for sleep duration
plt.bar(df['timestamp'], df['sleep_duration'], color='lightblue', alpha=0.7)
plt.axhline(7.5, color='r', linestyle='--', label='Ideal Sleep')
plt.title('Daily Sleep Duration')
plt.xticks(rotation=45)
plt.ylabel('Hours')
plt.legend()
plt.tight_layout()
plt.savefig('sleep_bar.png')
plt.show()

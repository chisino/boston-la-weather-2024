import pandas as pd
from datetime import datetime
from meteostat import Point, Daily
import matplotlib.pyplot as plt

# Set up the time range
start = datetime(2024, 1, 1)
end = datetime(2025, 1, 1)

# Define Points
boston = Point(42.3601, -71.0589, 43)
los_angeles = Point(34.0522, -118.2437, 93)

# Fetch data
bos_data = Daily(boston, start, end).fetch().loc[:, ['tavg', 'prcp']]
la_data = Daily(los_angeles, start, end).fetch().loc[:, ['tavg', 'prcp']]

# Rename columns to distinguish cities
bos_data = bos_data.rename(columns={'tavg': 'tavg_bos', 'prcp': 'prcp_bos'})
la_data = la_data.rename(columns={'tavg': 'tavg_la', 'prcp': 'prcp_la'})

# Convert Celsius to Fahrenheit
bos_data['tavg_bos'] = bos_data['tavg_bos'] * 9 / 5 + 32
la_data['tavg_la'] = la_data['tavg_la'] * 9 / 5 + 32

# Combine data on date
combined = pd.concat([bos_data, la_data], axis=1)

# Optional: Smooth with a rolling average (e.g., 7-day window)
combined_rolling = combined.rolling(window=7, min_periods=1).mean()

# Plot average temperature
plt.figure(figsize=(14, 6))
plt.plot(combined_rolling.index, combined_rolling['tavg_bos'], label='Boston Avg Temp (°F)', color='blue')
plt.plot(combined_rolling.index, combined_rolling['tavg_la'], label='LA Avg Temp (°F)', color='orange')
plt.title('7-Day Rolling Average Temperature (2024)')
plt.xlabel('Date')
plt.ylabel('Temperature (°C)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('temperature_comparison.png')
plt.show()

# Plot precipitation
plt.figure(figsize=(14, 6))
plt.plot(combined_rolling.index, combined_rolling['prcp_bos'], label='Boston Precipitation (mm)', color='blue')
plt.plot(combined_rolling.index, combined_rolling['prcp_la'], label='LA Precipitation (mm)', color='orange')
plt.title('7-Day Rolling Precipitation (2024)')
plt.xlabel('Date')
plt.ylabel('Precipitation (mm)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('precipitation_comparison.png')
plt.show()

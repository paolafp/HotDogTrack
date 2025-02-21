import tilemapbase
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Step 1: Initialize TileMapBase
tilemapbase.start_logging()
tilemapbase.init(create=True)

# Step 2: Load and clean GPS data
df_gps = pd.read_csv('/Hot Dog Track/csv/gps_data_2025-02-19.csv', parse_dates=['timestamp'])
df_gps = df_gps[(df_gps['latitude'] != 0) & (df_gps['longitude'] != 0)]
df_gps = df_gps.sort_values(by='timestamp')

# Step 3: Calculate time differences between consecutive points (in seconds)
df_gps['time_diff'] = df_gps['timestamp'].diff().dt.total_seconds()
df_gps['time_diff'].fillna(0, inplace=True)

# Step 4: Aggregate data by unique location to see:
# a) Total time spent at each spot, and b) the average speed there.
agg_data = df_gps.groupby(['latitude', 'longitude']).agg(
    total_time_spent=('time_diff', 'sum'),
    avg_speed=('Speed kmh', 'mean')
).reset_index()

# Project the aggregated coordinates to Web Mercator (one-by-one)
agg_data['x'] = agg_data.apply(lambda row: tilemapbase.project(row['longitude'], row['latitude'])[0], axis=1)
agg_data['y'] = agg_data.apply(lambda row: tilemapbase.project(row['longitude'], row['latitude'])[1], axis=1)

# Step 5: Build map extent using the raw lat/lon (with a buffer)
buffer = 0.001  # ~100 meters buffer in degrees
extent = tilemapbase.Extent.from_lonlat(
    df_gps['longitude'].min() - buffer,
    df_gps['longitude'].max() + buffer,
    df_gps['latitude'].min() - buffer,
    df_gps['latitude'].max() + buffer
)

# Step 6: Create and plot the base map using OSM tiles
fig, ax = plt.subplots(figsize=(32, 18))
osm_tiles = tilemapbase.tiles.build_OSM()
plotter = tilemapbase.Plotter(extent, osm_tiles, width=1000)
plotter.plot(ax, allow_large=True)

# Remove axis labels
ax.set_yticks([])
ax.set_xticks([])

# Step 7: Plot the aggregated points on the map 
# Marker size (s) is scaled from total_time_spent (in seconds).
# Adjust scaling_factor as needed for good visual sizes.
scaling_factor = 2
scatter = ax.scatter(
    agg_data['x'], agg_data['y'],
    s=agg_data['total_time_spent'] / scaling_factor,
    c=agg_data['avg_speed'], cmap='viridis_r',
    alpha=0.8,
    label='Aggregated Spots'
)

# Step 8: Add colorbar and title
plt.colorbar(scatter, label='Average Speed (km/h)')
ax.set_title("GPS Track Aggregated by Location\nMarker Size: Total Time Spent (s), Marker Color: Average Speed (km/h)")
plt.legend()
plt.show()

import pandas as pd
import folium

# Read CSV file with proper parsing
csv_path = r'C:/Users/Paola/kDrive/BHT/Geosensorik/Hot Dog Track/csv/gps_data_2025-02-19.csv'
gps_df = pd.read_csv(csv_path)

# Convert coordinates to numeric and clean data
gps_df['latitude'] = pd.to_numeric(gps_df['latitude'], errors='coerce')
gps_df['longitude'] = pd.to_numeric(gps_df['longitude'], errors='coerce')

# Remove invalid entries (NaNs and 0.0 coordinates)
gps_df = gps_df.dropna(subset=['latitude', 'longitude'])
gps_df = gps_df[~((gps_df['latitude'] == 0.0) & (gps_df['longitude'] == 0.0))]

# Create map only if valid data remains
if not gps_df.empty:
    # Calculate dynamic zoom based on coordinate spread
    lat_range = gps_df['latitude'].max() - gps_df['latitude'].min()
    lon_range = gps_df['longitude'].max() - gps_df['longitude'].min()
    zoom_level = 18 if max(lat_range, lon_range) < 0.001 else 14
    
    # Create map with automatic bounds
    m = folium.Map(
        location=[gps_df['latitude'].mean(), gps_df['longitude'].mean()],
        zoom_start=zoom_level,
        control_scale=True
    )
    
    # Add track with optimized rendering
    coordinates = gps_df[['latitude', 'longitude']].values.tolist()
    folium.PolyLine(
        coordinates,
        weight=4,
        color='#FF0000',
        opacity=0.9,
        smooth_factor=2
    ).add_to(m)
    
    # Add enhanced markers
    if len(coordinates) > 0:
        folium.Marker(
            coordinates[0],
            popup=folium.Popup(f"Start<br>{coordinates[0]}", max_width=250),
            icon=folium.Icon(color='green', prefix='fa', icon='play')
        ).add_to(m)
        
        folium.Marker(
            coordinates[-1],
            popup=folium.Popup(f"End<br>{coordinates[-1]}", max_width=250),
            icon=folium.Icon(color='red', prefix='fa', icon='flag-checkered')
        ).add_to(m)
    
    # Save map with proper encoding
    m.save('gps_track.html')
    print("Map successfully created with filtered data")
else:
    print("No valid GPS coordinates remaining after filtering")

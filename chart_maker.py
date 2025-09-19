# chart_maker.py
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

def create_temperature_map(data, title="Ocean Temperature"):
    """Create an interactive temperature heatmap"""
    try:
        # Get the most recent time slice
        if len(data.shape) == 3:  # time, lat, lon
            latest_data = data[-1, :, :]  # Most recent time
        else:
            latest_data = data
            
        # Get coordinates
        lats = data.latitude.values if hasattr(data, 'latitude') else np.linspace(5, 25, latest_data.shape[0])
        lons = data.longitude.values if hasattr(data, 'longitude') else np.linspace(80, 100, latest_data.shape[1])
        
        # Create heatmap
        fig = go.Figure(data=go.Heatmap(
            z=latest_data.values,
            x=lons,
            y=lats,
            colorscale='Viridis',
            colorbar=dict(title="Temperature (°C)"),
            hovertemplate='Longitude: %{x}<br>Latitude: %{y}<br>Temperature: %{z:.2f}°C<extra></extra>'
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Longitude",
            yaxis_title="Latitude",
            width=700,
            height=500,
            font=dict(color="#006989")
        )
        
        return fig
        
    except Exception as e:
        print(f"❌ Error creating temperature map: {e}")
        return None

def create_simple_line_chart(data, title="Ocean Data Trend"):
    """Create a simple line chart showing data over time"""
    try:
        # Calculate average over space for each time step
        if len(data.shape) == 3:  # time, lat, lon
            time_series = data.mean(dim=['latitude', 'longitude'])
        else:
            time_series = data.mean()
            
        # Get time coordinates
        if hasattr(data, 'time'):
            times = data.time.values
        else:
            times = pd.date_range('2024-01-01', periods=len(time_series), freq='D')
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=times,
            y=time_series.values,
            mode='lines+markers',
            name='Average Value',
            line=dict(color='#006989', width=3),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            title=title,
            xaxis_title="Time",
            yaxis_title="Value",
            width=700,
            height=400,
            font=dict(color="#006989")
        )
        
        return fig
        
    except Exception as e:
        print(f"❌ Error creating line chart: {e}")
        return None

def create_stats_chart(stats, parameter="Temperature"):
    """Create a simple bar chart of statistics"""
    try:
        categories = ['Minimum', 'Average', 'Maximum']
        values = [stats['min'], stats['mean'], stats['max']]
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color='#006989',
                text=[f'{v:.2f}°C' for v in values],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title=f"{parameter} Statistics",
            yaxis_title=f"{parameter} (°C)",
            width=500,
            height=400,
            font=dict(color="#006989")
        )
        
        return fig
        
    except Exception as e:
        print(f"❌ Error creating stats chart: {e}")
        return None

# Test the chart maker
if __name__ == "__main__":
    from data_handler import load_ocean_data, filter_data, get_simple_stats
    
    # Load data
    ds = load_ocean_data()
    temp_data = filter_data(ds, "temperature", "bay of bengal")
    
    if temp_data is not None:
        # Test different charts
        print("Creating temperature map...")
        temp_map = create_temperature_map(temp_data, "Bay of Bengal Temperature")
        
        print("Creating line chart...")
        line_chart = create_simple_line_chart(temp_data, "Temperature Trend")
        
        print("Creating stats chart...")
        stats = get_simple_stats(temp_data)
        stats_chart = create_stats_chart(stats, "Temperature")
        
        print("✅ All charts created successfully!")
        
        # You can save charts as HTML to test them
        if temp_map:
            temp_map.write_html("test_temp_map.html")
            print("💾 Saved test_temp_map.html")
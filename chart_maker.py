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

def create_3d_surface_plot(data, title="Ocean Data 3D View"):
    """Create a 3D surface plot of ocean data"""
    try:
        # Get the most recent time slice
        if len(data.shape) == 3:
            latest_data = data[-1, :, :]
        else:
            latest_data = data
            
        # Get coordinates
        lats = data.latitude.values if hasattr(data, 'latitude') else np.linspace(5, 25, latest_data.shape[0])
        lons = data.longitude.values if hasattr(data, 'longitude') else np.linspace(80, 100, latest_data.shape[1])
        
        # Create meshgrid for 3D plotting
        lon_mesh, lat_mesh = np.meshgrid(lons, lats)
        
        fig = go.Figure(data=[go.Surface(
            z=latest_data.values,
            x=lon_mesh,
            y=lat_mesh,
            colorscale='Viridis',
            hovertemplate='Longitude: %{x:.2f}°<br>Latitude: %{y:.2f}°<br>Value: %{z:.2f}<extra></extra>'
        )])
        
        fig.update_layout(
            title=f"🌐 {title} - 3D Surface View",
            scene=dict(
                xaxis_title="Longitude (°)",
                yaxis_title="Latitude (°)",
                zaxis_title="Value",
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))
            ),
            width=800,
            height=600,
            font=dict(color="#006989")
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating 3D surface plot: {e}")
        return None


def create_contour_map(data, title="Ocean Data Contours"):
    """Create a contour map with isolines"""
    try:
        # Get the most recent time slice
        if len(data.shape) == 3:
            latest_data = data[-1, :, :]
        else:
            latest_data = data
            
        # Get coordinates
        lats = data.latitude.values if hasattr(data, 'latitude') else np.linspace(5, 25, latest_data.shape[0])
        lons = data.longitude.values if hasattr(data, 'longitude') else np.linspace(80, 100, latest_data.shape[1])
        
        fig = go.Figure()
        
        # Add filled contours
        fig.add_trace(go.Contour(
            z=latest_data.values,
            x=lons,
            y=lats,
            colorscale='Viridis',
            contours=dict(
                showlabels=True,
                labelfont=dict(size=12, color='white')
            ),
            hovertemplate='Longitude: %{x:.2f}°<br>Latitude: %{y:.2f}°<br>Value: %{z:.2f}<extra></extra>'
        ))
        
        fig.update_layout(
            title=f"📈 {title} - Contour Map",
            xaxis_title="Longitude (°)",
            yaxis_title="Latitude (°)",
            width=800,
            height=600,
            font=dict(color="#006989")
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating contour map: {e}")
        return None
    
    
def create_comparison_chart(temp_data, salt_data, region_name):
    """Create side-by-side comparison of temperature and salinity"""
    try:
        from plotly.subplots import make_subplots
        
        # Get latest data
        if len(temp_data.shape) == 3:
            latest_temp = temp_data[-1, :, :]
            latest_salt = salt_data[-1, :, :]
        else:
            latest_temp = temp_data
            latest_salt = salt_data
        
        # Get coordinates
        lats = temp_data.latitude.values if hasattr(temp_data, 'latitude') else np.linspace(5, 25, latest_temp.shape[0])
        lons = temp_data.longitude.values if hasattr(temp_data, 'longitude') else np.linspace(80, 100, latest_temp.shape[1])
        
        # Create subplots
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=('Temperature (°C)', 'Salinity (PSU)'),
            specs=[[{"type": "heatmap"}, {"type": "heatmap"}]]
        )
        
        # Add temperature heatmap
        fig.add_trace(
            go.Heatmap(
                z=latest_temp.values,
                x=lons,
                y=lats,
                colorscale='RdYlBu_r',
                name='Temperature',
                hovertemplate='Lon: %{x:.1f}°<br>Lat: %{y:.1f}°<br>Temp: %{z:.1f}°C<extra></extra>'
            ),
            row=1, col=1
        )
        
        # Add salinity heatmap
        fig.add_trace(
            go.Heatmap(
                z=latest_salt.values,
                x=lons,
                y=lats,
                colorscale='Viridis',
                name='Salinity',
                hovertemplate='Lon: %{x:.1f}°<br>Lat: %{y:.1f}°<br>Salinity: %{z:.1f} PSU<extra></extra>'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            title=f"🌊 Temperature & Salinity Comparison - {region_name.title()}",
            width=1000,
            height=500,
            font=dict(color="#006989")
        )
        
        return fig
        
    except Exception as e:
        print(f"Error creating comparison chart: {e}")
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
            


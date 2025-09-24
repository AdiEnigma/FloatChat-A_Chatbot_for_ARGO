# data_handler.py
import xarray as xr
import pandas as pd
import numpy as np
import requests
import os

def download_sample_data():
    """Download a small sample Argo dataset"""
    # Sample Argo data URL (this is a real, small Argo file)
    url = "https://data-argo.ifremer.fr/geo/indian_ocean/2023/12/D5906241_001.nc"
    filename = "sample_argo_data.nc"
    
    if not os.path.exists(filename):
        print("Downloading sample Argo data...")
        try:
            response = requests.get(url, timeout=30)
            with open(filename, 'wb') as f:
                f.write(response.content)
            print("✅ Sample data downloaded!")
            return filename
        except:
            print("⚠️  Download failed, using dummy data instead")
            return create_dummy_data()
    else:
        print("✅ Sample data already exists!")
        return filename

# In data_handler.py, replace the old create_dummy_data function with this one.

def create_dummy_data():
    """Create realistic dummy ocean data with seasonal variation"""
    print("Creating comprehensive dummy ocean data with seasonal patterns...")
    
    # Define realistic ranges for each region
    regions = {
        'bay_of_bengal': {
            'lat_range': (5, 25), 'lon_range': (80, 100),
            'temp_range': (24, 30), 'salt_range': (32, 35),
            'seasonal_temp_var': 3  # 3°C seasonal variation
        },
        'arabian_sea': {
            'lat_range': (5, 25), 'lon_range': (50, 80),
            'temp_range': (22, 29), 'salt_range': (35, 37),
            'seasonal_temp_var': 4
        },
        'pacific_ocean': {
            'lat_range': (-40, 60), 'lon_range': (120, 240),
            'temp_range': (2, 30), 'salt_range': (32, 36),
            'seasonal_temp_var': 8  # Large ocean, more variation
        },
        'atlantic_ocean': {
            'lat_range': (-60, 70), 'lon_range': (280, 380),
            'temp_range': (0, 28), 'salt_range': (33, 37),
            'seasonal_temp_var': 10
        },
        'indian_ocean': {
            'lat_range': (-50, 30), 'lon_range': (20, 120),
            'temp_range': (5, 32), 'salt_range': (33, 37),
            'seasonal_temp_var': 6
        },
        'mediterranean_sea': {
            'lat_range': (30, 46), 'lon_range': (-5, 36),
            'temp_range': (13, 28), 'salt_range': (36, 39),
            'seasonal_temp_var': 8  # Strong seasonal variation
        },
        'arctic_ocean': {
            'lat_range': (65, 90), 'lon_range': (-180, 180),
            'temp_range': (-2, 8), 'salt_range': (28, 35),
            'seasonal_temp_var': 12  # Extreme seasonal variation
        }
    }
    
    # Create comprehensive coordinate system
    all_lats = np.linspace(-60, 90, 100)
    all_lons = np.linspace(-180, 360, 150)
    times = pd.date_range('2024-01-01', periods=10, freq='D')
    
    # Initialize global arrays
    temp_data = np.full((10, 100, 150), np.nan)
    salt_data = np.full((10, 100, 150), np.nan)
    
    # Fill data for each region
    for region_name, config in regions.items():
        lat_mask = (all_lats >= config['lat_range'][0]) & (all_lats <= config['lat_range'][1])
        
        if config['lon_range'][1] > 180:
            lon_mask = (all_lons >= config['lon_range'][0]) | (all_lons <= config['lon_range'][1] - 360)
        else:
            lon_mask = (all_lons >= config['lon_range'][0]) & (all_lons <= config['lon_range'][1])
        
        lat_indices = np.where(lat_mask)[0]
        lon_indices = np.where(lon_mask)[0]
        
        region_temp_base = (config['temp_range'][0] + config['temp_range'][1]) / 2
        region_temp_var = (config['temp_range'][1] - config['temp_range'][0]) / 2
        region_salt_base = (config['salt_range'][0] + config['salt_range'][1]) / 2
        region_salt_var = (config['salt_range'][1] - config['salt_range'][0]) / 2
        
        for t in range(10):
            # Add seasonal variation (simulate January effect)
            day_of_year = 1 + t  # January 1st + t days
            seasonal_factor = np.sin((day_of_year / 365.0) * 2 * np.pi - np.pi/2)  # Winter in January
            
            for i, lat_idx in enumerate(lat_indices):
                for j, lon_idx in enumerate(lon_indices):
                    lat_value = all_lats[lat_idx]
                    
                    # Latitude-based temperature gradient
                    lat_temp_effect = (90 - abs(lat_value)) / 90.0 * 15  # Warmer near equator
                    
                    # Seasonal effect (stronger at higher latitudes)
                    seasonal_effect = seasonal_factor * config['seasonal_temp_var'] * (abs(lat_value) / 90.0)
                    
                    # Random variation
                    temp_variation = np.random.normal(0, region_temp_var * 0.2)
                    salt_variation = np.random.normal(0, region_salt_var * 0.2)
                    
                    # Final temperature with all effects
                    final_temp = region_temp_base + lat_temp_effect + seasonal_effect + temp_variation
                    final_salt = region_salt_base + salt_variation
                    
                    temp_data[t, lat_idx, lon_idx] = final_temp
                    salt_data[t, lat_idx, lon_idx] = final_salt
    
    # Create xarray dataset
    ds = xr.Dataset({
        'temperature': (['time', 'latitude', 'longitude'], temp_data),
        'salinity': (['time', 'latitude', 'longitude'], salt_data)
    }, coords={
        'time': times,
        'latitude': all_lats,
        'longitude': all_lons
    })
    
    ds.to_netcdf('comprehensive_dummy_data.nc')
    print("✅ Enhanced realistic dummy data created with seasonal and latitude effects!")
    return 'comprehensive_dummy_data.nc'

def load_ocean_data():
    """Load and return ocean dataset"""
    try:
        # First try the real data
        if os.path.exists('sample_argo_data.nc'):
            try:
                ds = xr.open_dataset('sample_argo_data.nc', engine='h5netcdf')
                print(f"✅ Loaded real Argo data with variables: {list(ds.data_vars)}")
                return ds
            except:
                print("⚠️  Real data failed to load, using dummy data")
        
        # Fallback to dummy data
        filename = create_dummy_data()
        ds = xr.open_dataset(filename)
        print(f"✅ Loaded dummy data with variables: {list(ds.data_vars)}")
        return ds
        
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def filter_data(ds, parameter, region=None, time_range=None):
    """Filter ocean data based on parameters with expanded regions"""
    try:
        if ds is None:
            return None
            
        # Expanded region filtering
        filtered_ds = ds
        if region:
            region_lower = region.lower()
            if "bengal" in region_lower:
                filtered_ds = ds.sel(latitude=slice(5, 25), longitude=slice(80, 100))
            elif "arabian" in region_lower:
                filtered_ds = ds.sel(latitude=slice(5, 25), longitude=slice(50, 80))
            elif "pacific" in region_lower:
                filtered_ds = ds.sel(latitude=slice(-40, 60), longitude=slice(120, 240))
            elif "atlantic" in region_lower:
                filtered_ds = ds.sel(latitude=slice(-60, 70), longitude=slice(280, 380))
            elif "indian" in region_lower and "ocean" in region_lower:
                filtered_ds = ds.sel(latitude=slice(-50, 30), longitude=slice(20, 120))
            elif "mediterranean" in region_lower:
                filtered_ds = ds.sel(latitude=slice(30, 46), longitude=slice(-5, 36))
            elif "arctic" in region_lower:
                filtered_ds = ds.sel(latitude=slice(65, 90), longitude=slice(-180, 180))
            
        # Get the requested parameter
        if parameter.lower() == 'temperature' and 'temperature' in filtered_ds:
            data = filtered_ds['temperature']
        elif parameter.lower() == 'salinity' and 'salinity' in filtered_ds:
            data = filtered_ds['salinity']
        else:
            # Try to find any temperature-like variable
            temp_vars = [var for var in filtered_ds.data_vars if 'temp' in var.lower()]
            if temp_vars:
                data = filtered_ds[temp_vars[0]]
            else:
                var_name = list(filtered_ds.data_vars)[0]
                data = filtered_ds[var_name]
                print(f"Using variable: {var_name}")
                
        # Remove NaN values (areas with no data)
        data = data.where(~np.isnan(data), drop=True)
        
        return data
        
    except Exception as e:
        print(f"❌ Error filtering data: {e}")
        return None

def get_simple_stats(data):
    """Get basic statistics from the data"""
    if data is None:
        return None
        
    try:
        stats = {
            'mean': float(data.mean().values),
            'min': float(data.min().values),
            'max': float(data.max().values),
            'shape': data.shape
        }
        return stats
    except Exception as e:
        print(f"❌ Error computing stats: {e}")
        return None

# Test the data handler
if __name__ == "__main__":
    ds = load_ocean_data()
    if ds is not None:
        temp_data = filter_data(ds, "temperature", "bay of bengal")
        if temp_data is not None:
            stats = get_simple_stats(temp_data)
            print(f"✅ Success! Data shape: {temp_data.shape}")
            print(f"📊 Stats: {stats}")
        else:
            print("❌ Failed to filter data")
    else:
        print("❌ Failed to load data")
        

def get_enhanced_stats(data, region_name="Unknown Region"):
    """Get enhanced statistics with regional context"""
    if data is None:
        return None
        
    try:
        # Basic stats
        stats = {
            'mean': float(data.mean().values),
            'min': float(data.min().values),
            'max': float(data.max().values),
            'std': float(data.std().values),
            'shape': data.shape,
            'region': region_name,
            'data_points': int(np.sum(~np.isnan(data.values))),
        }
        
        # Regional context
        region_context = {
            'bay of bengal': 'Tropical region with monsoon effects',
            'arabian sea': 'High evaporation, elevated salinity',
            'pacific ocean': 'World\'s largest ocean with diverse conditions',
            'atlantic ocean': 'Meridional circulation patterns',
            'indian ocean': 'Monsoon-driven seasonal patterns',
            'mediterranean sea': 'Enclosed sea with high salinity',
            'arctic ocean': 'Ice-covered, extreme seasonal variation',
        }
        
        stats['description'] = region_context.get(region_name.lower(), 'Ocean region')
        return stats
        
    except Exception as e:
        print(f"❌ Error computing enhanced stats: {e}")
        return None
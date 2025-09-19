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

def create_dummy_data():
    """Create dummy ocean data if download fails"""
    print("Creating dummy ocean data...")
    
    # Create sample coordinates
    lats = np.linspace(5, 25, 20)  # Bay of Bengal region
    lons = np.linspace(80, 100, 20)
    times = pd.date_range('2024-01-01', periods=10, freq='D')
    
    # Create dummy temperature and salinity data
    temp_data = 25 + 5 * np.random.random((10, 20, 20))  # 20-30°C
    salt_data = 34 + 2 * np.random.random((10, 20, 20))  # 34-36 PSU
    
    # Create xarray dataset
    ds = xr.Dataset({
        'temperature': (['time', 'latitude', 'longitude'], temp_data),
        'salinity': (['time', 'latitude', 'longitude'], salt_data)
    }, coords={
        'time': times,
        'latitude': lats,
        'longitude': lons
    })
    
    # Save as NetCDF file
    ds.to_netcdf('dummy_argo_data.nc')
    print("✅ Dummy data created!")
    return 'dummy_argo_data.nc'

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
    """Filter ocean data based on parameters"""
    try:
        if ds is None:
            return None
            
        # Simple region filtering - FIXED the slice issue
        filtered_ds = ds
        if region and "bengal" in region.lower():
            # Bay of Bengal approximate coordinates
            filtered_ds = ds.sel(latitude=slice(5, 25), longitude=slice(80, 100))
        elif region and "arabian" in region.lower():
            # Arabian Sea approximate coordinates  
            filtered_ds = ds.sel(latitude=slice(5, 25), longitude=slice(65, 80))
            
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
                # Just get first available variable
                var_name = list(filtered_ds.data_vars)[0]
                data = filtered_ds[var_name]
                print(f"Using variable: {var_name}")
                
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
#!/usr/bin/env python3
"""
Test script to verify SolidSphere module functionality.
"""

import sys
from pathlib import Path
import numpy as np

# Add project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

print("Testing SolidSphere integration...")

try:
    # Test imports
    from utils.SeaEcho_water import seawater
    from utils.SeaEcho_solid_sphere import Tungsten_carbide, Copper
    from SolidSphere.models.SeaEcho_TS_SolidSphere import TS_solid_sphere
    from SolidSphere.core.io_utils import plot_ts_vs_frequency
    
    print("✅ All SolidSphere imports successful")
    
    # Test water properties
    water = seawater(temperature=10, depth=100, salinity=35)
    print(f"✅ Water properties:")
    print(f"    Sound speed = {water.c:.2f} m/s")
    print(f"    Density = {water.rho:.2f} kg/m³")
    
    # Test material properties
    wc_material = Tungsten_carbide()
    copper_material = Copper()
    
    print(f"✅ Material properties:")
    print(f"    Tungsten Carbide: density = {wc_material.rho:.0f} kg/m³, speed = {wc_material.c_lon:.0f} m/s")
    print(f"    Copper: density = {copper_material.rho:.0f} kg/m³, speed = {copper_material.c_lon:.0f} m/s")
    
    # Test TS calculation
    test_frequency = 18.0  # kHz
    test_radius = 0.005    # 5 mm radius
    
    # Calculate TS for both materials
    ts_wc = float(TS_solid_sphere(test_frequency, test_radius, wc_material, water))
    ts_copper = float(TS_solid_sphere(test_frequency, test_radius, copper_material, water))
    
    print(f"✅ Target Strength calculations at {test_frequency} kHz, {test_radius*1000} mm radius:")
    print(f"    Tungsten Carbide TS = {ts_wc:.2f} dB")
    print(f"    Copper TS = {ts_copper:.2f} dB")
    
    # Validate TS values are reasonable
    if -80 <= ts_wc <= -40 and -80 <= ts_copper <= -40:
        print("✅ TS values are within expected range")
    else:
        print("❌ TS values are outside expected range")
        
    # Test frequency sweep calculation
    frequencies = np.linspace(10, 50, 5)  # Small test range
    ts_results_wc = []
    ts_results_copper = []
    
    for freq in frequencies:
        ts_wc = float(TS_solid_sphere(freq, test_radius, wc_material, water))
        ts_copper = float(TS_solid_sphere(freq, test_radius, copper_material, water))
        ts_results_wc.append(ts_wc)
        ts_results_copper.append(ts_copper)
    
    print(f"✅ Frequency sweep calculation successful:")
    print(f"    WC TS range: {min(ts_results_wc):.2f} to {max(ts_results_wc):.2f} dB")
    print(f"    Copper TS range: {min(ts_results_copper):.2f} to {max(ts_results_copper):.2f} dB")
    
    # Test plotting function (without actually displaying/saving)
    try:
        ts_results = {
            "Tungsten Carbide": ts_results_wc,
            "Copper": ts_results_copper
        }
        
        # Test plot creation (but don't save or show)
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend for testing
        
        plot_ts_vs_frequency(frequencies, ts_results, test_radius*1000, 
                           labels=None, filename=None, show_plot=False, save_plot=False)
        print("✅ Plotting function works correctly")
        
    except Exception as e:
        print(f"❌ Plotting error: {e}")
    
    # Test edge cases
    try:
        # Very small sphere
        ts_small = float(TS_solid_sphere(test_frequency, 0.001, wc_material, water))  # 1 mm radius
        
        # Very large sphere  
        ts_large = float(TS_solid_sphere(test_frequency, 0.01, wc_material, water))   # 10 mm radius
        
        print(f"✅ Edge case calculations:")
        print(f"    Small sphere (1 mm): {ts_small:.2f} dB")
        print(f"    Large sphere (10 mm): {ts_large:.2f} dB")
        
        # TS should increase with sphere size
        if ts_large > ts_small:
            print("✅ TS increases with sphere size as expected")
        else:
            print("❌ Unexpected TS size relationship")
            
    except Exception as e:
        print(f"❌ Edge case error: {e}")
    
    print("\n🎉 SolidSphere module testing complete!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
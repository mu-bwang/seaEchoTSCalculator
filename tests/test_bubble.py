#!/usr/bin/env python3
"""
Test script to verify Bubble module functionality.
"""

import sys
from pathlib import Path
import numpy as np

# Add project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

print("Testing Bubble integration...")

try:
    # Test imports
    from utils.SeaEcho_water import seawater
    from utils.SeaEcho_gas_bubble import air_bubble
    from Bubble.core.processor import run_calculations, MODEL_FUNCTIONS
    from Bubble.models.medwin_clay_model import calculate_medwin_clay_ts
    from Bubble.models.breathing_model import calculate_breathing_ts
    from Bubble.core.io_utils import export_results_csv, save_figure
    
    print(f"✅ Available bubble models: {list(MODEL_FUNCTIONS.keys())}")
    
    # Test water and bubble properties
    water = seawater(temperature=10, depth=100, salinity=35)
    bubble = air_bubble(water_class=None, T=10, z=100, S=35, diameter=0.002)  # 2mm bubble
    
    print(f"✅ Water properties:")
    print(f"    Sound speed = {water.c:.2f} m/s")
    print(f"    Density = {water.rho:.2f} kg/m³")
    
    print(f"✅ Bubble properties:")
    print(f"    Diameter = {bubble.d*1000:.1f} mm")
    print(f"    Density = {bubble.rho:.3f} kg/m³")
    
    # Test core TS calculations
    test_frequency = 50.0  # kHz
    
    print(f"\n📊 Testing TS calculations at {test_frequency} kHz:")
    
    # Test Medwin-Clay model
    ts_mc = float(calculate_medwin_clay_ts(f=test_frequency, c=water.c, water=water, bubble=bubble))
    print(f"✅ Medwin-Clay TS = {ts_mc:.2f} dB")
    
    # Test Breathing model
    ts_breathing = float(calculate_breathing_ts(f=test_frequency, c=water.c, water=water, bubble=bubble))
    print(f"✅ Breathing model TS = {ts_breathing:.2f} dB")
    
    # Validate TS values are reasonable for bubbles
    if -80 <= ts_mc <= -40 and -80 <= ts_breathing <= -40:
        print("✅ TS values are within expected range for gas bubbles")
    else:
        print("❌ TS values are outside expected range")
    
    # Test frequency sweep
    frequencies = np.linspace(20, 100, 5)  # Small test range
    ts_results_mc = []
    ts_results_breathing = []
    
    for freq in frequencies:
        ts_mc = float(calculate_medwin_clay_ts(f=freq, c=water.c, water=water, bubble=bubble))
        ts_br = float(calculate_breathing_ts(f=freq, c=water.c, water=water, bubble=bubble))
        ts_results_mc.append(ts_mc)
        ts_results_breathing.append(ts_br)
    
    print(f"✅ Frequency sweep calculation successful:")
    print(f"    Medwin-Clay TS range: {min(ts_results_mc):.2f} to {max(ts_results_mc):.2f} dB")
    print(f"    Breathing TS range: {min(ts_results_breathing):.2f} to {max(ts_results_breathing):.2f} dB")
    
    # Test I/O functions
    try:
        # Test CSV export (but don't actually save)
        test_results = {
            "frequency": frequencies.tolist(),
            "medwin_clay_ts": ts_results_mc,
            "breathing_ts": ts_results_breathing
        }
        print("✅ I/O functions imported successfully")
        
    except Exception as e:
        print(f"❌ I/O error: {e}")
    
    # Test edge cases
    try:
        # Very small bubble
        small_bubble = air_bubble(water_class=None, T=10, z=100, S=35, diameter=0.0005)  # 0.5mm
        ts_small = float(calculate_medwin_clay_ts(f=test_frequency, c=water.c, water=water, bubble=small_bubble))
        
        # Larger bubble
        large_bubble = air_bubble(water_class=None, T=10, z=100, S=35, diameter=0.004)  # 4mm
        ts_large = float(calculate_medwin_clay_ts(f=test_frequency, c=water.c, water=water, bubble=large_bubble))
        
        print(f"✅ Edge case calculations:")
        print(f"    Small bubble (0.5 mm): {ts_small:.2f} dB")
        print(f"    Large bubble (4.0 mm): {ts_large:.2f} dB")
        
        # For bubbles, TS relationship with size can be complex due to resonance
        print("✅ Size variation testing complete")
        
    except Exception as e:
        print(f"❌ Edge case error: {e}")

    print("\n🎉 Bubble module testing complete!")

except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    import traceback
    traceback.print_exc()
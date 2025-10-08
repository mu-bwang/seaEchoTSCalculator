#!/usr/bin/env python3
"""
Test script to verify all utils files work together properly.
"""

import sys
from pathlib import Path

# Add project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

print("Testing utils integration...")

try:
    # Test SeaEcho_water
    from utils.SeaEcho_water import seawater
    water = seawater(temperature=8, depth=1000, salinity=35)
    print(f"✅ SeaEcho_water properties:")
    print(f"    Sound speed = {water.c:.2f} m/s")
    print(f"    Density = {water.rho:.2f} kg/m³")
    print(f"    Temperature = {water.T}°C")
    print(f"    Depth = {water.z} m")
    print(f"    Salinity = {water.S} psu")
    print(f"    Pressure = {water.P/1e5:.2f} bar")
    print(f"    Dynamic viscosity = {water.mu:.6f} Pa·s")
    print(f"    Kinematic viscosity = {water.nu:.8f} m²/s")
    print(f"    Surface tension = {water.sigma:.4f} N/m")
    
    # Test SeaEcho_solid_sphere
    from utils.SeaEcho_solid_sphere import Tungsten_carbide, Copper
    tungsten = Tungsten_carbide()
    copper = Copper()
    print(f"✅ SeaEcho_solid_sphere: Tungsten_carbide density = {tungsten.rho} kg/m³")
    print(f"✅ SeaEcho_solid_sphere: Copper density = {copper.rho} kg/m³")
    
    # Test SeaEcho_gas_bubble
    from utils.SeaEcho_gas_bubble import air_bubble
    bubble = air_bubble(water_class=None, T=10, z=100, S=35, diameter=0.001)  # 1mm bubble
    print(f"✅ SeaEcho_gas_bubble properties:")
    print(f"    Bubble diameter = {bubble.d*1000:.1f} mm")
    print(f"    Bubble density = {bubble.rho:.3f} kg/m³")
    print(f"    Bubble density at sea level = {bubble.rho_0:.3f} kg/m³")
    print(f"    Gas pressure inside bubble = {bubble.Pg/1e5:.2f} bar")
    print(f"    Specific heat ratio (gamma) = {bubble.gamma}")
    print(f"    Molecular mass = {bubble.Mm*1000:.2f} g/mol")
    print(f"    Specific heat capacity = {bubble.Cp:.3f} kJ/(kg·K)")
    print(f"    Thermal conductivity = {bubble.K_th:.6f} W/(m·K)")
    
    # Test SeaEcho_acoustic_paras
    from utils.SeaEcho_acoustic_paras import resonance_freq, damping_constant
    f_b, f_R, corrections = resonance_freq(f=50, c=water.c, water=water, bubble=bubble)
    damping = damping_constant(f=50, c=water.c, water=water, bubble=bubble)
    print(f"✅ SeaEcho_acoustic_paras: Resonance freq = {float(f_R):.1f} Hz")
    print(f"✅ SeaEcho_acoustic_paras: Damping = {float(damping):.6f}")
    
    print("\n🎉 All utils files working properly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
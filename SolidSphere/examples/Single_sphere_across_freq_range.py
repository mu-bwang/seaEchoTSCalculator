"""
Target Strength Calculation for Tungsten Carbide Sphere

This example demonstrates how to calculate the acoustic target strength (TS) of a 
tungsten carbide solid sphere across a range of sonar frequencies. The calculation 
uses the modal solution for elastic sphere scattering in seawater.

The script calculates TS values for a sphere with user-defined parameters including:
- Environmental conditions (temperature, salinity, depth)  
- Sphere radius
- Frequency range

Results are plotted and saved as a PNG file showing TS vs frequency response.
"""

from concurrent.futures import ProcessPoolExecutor
import numpy as np
import sys
from pathlib import Path

# Add paths for proper imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # …/SolidSphere
MAIN_ROOT = Path(__file__).resolve().parents[2]     # …/seaEchoTSCalculator
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(MAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(MAIN_ROOT))

from utils.SeaEcho_water import seawater
from utils.SeaEcho_solid_sphere import Tungsten_carbide
from models.SeaEcho_TS_SolidSphere import TS_solid_sphere
from core.io_utils import plot_ts_vs_frequency



def main():
    # User-defined parameters
    T = 10  # Temperature in °C
    S = 35  # Salinity in psu
    z = 100  # Depth in meters
    radius_mm = 5  # Sphere radius in mm
    radius = radius_mm / 1000  # Convert to meters
    sonar_frequencies = np.linspace(10, 1000, 300)  # Frequencies in kHz

    """
    User should modify the above parameters as needed.
    """

    # Create seawater and material objects
    water = seawater(T, z, S)
    WC = Tungsten_carbide()
    
    # Report water sound speed
    print(f"\nWater Properties:")
    print(f"  Temperature: {T}°C")
    print(f"  Salinity: {S} psu")
    print(f"  Depth: {z} m")
    print(f"  Sound speed in water: {water.c:.2f} m/s")
    print(f"  Water density: {water.rho:.2f} kg/m³")

    # Use ProcessPoolExecutor to parallelize frequency computations
    with ProcessPoolExecutor() as executor:
        TS = list(executor.map(TS_solid_sphere, sonar_frequencies,
                                        [radius] * len(sonar_frequencies),
                                        [WC] * len(sonar_frequencies),
                                        [water] * len(sonar_frequencies)))

    # Convert results to numpy array and regular floats
    TS = np.array([float(ts) for ts in TS])

    """
    User can uncomment below print statements as needed
    """
    # ---------
    # print("Target Strength (dB):")
    # for i, (freq, ts) in enumerate(zip(sonar_frequencies, TS)):
    #   print(f"  {freq} kHz: {ts:.2f} dB")
    # ---------

    # Create plot using plot_utils
    ts_results = {"WC Sphere": TS.tolist()}
    # Save plot in the current examples directory
    current_dir = Path(__file__).parent
    plot_filename = current_dir / "WC_sphere_results.png"
    plot_ts_vs_frequency(sonar_frequencies, ts_results, radius_mm, labels=None,
                        filename=plot_filename, show_plot=True, save_plot=True)
    print(f"\nPlot saved as WC_sphere_results.png in the examples directory")
    print("Plot window should be displayed - close it to continue.")


if __name__ == '__main__':
    main()



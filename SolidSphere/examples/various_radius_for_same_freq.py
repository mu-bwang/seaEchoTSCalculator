"""
Target Strength Calculation for Various Tungsten Carbide Sphere Radii

This example demonstrates how to calculate the acoustic target strength (TS) of 
tungsten carbide solid spheres of various radii at a single sonar frequency. 
The calculation uses the modal solution for elastic sphere scattering in seawater.

The script calculates TS values for spheres with user-defined parameters including:
- Environmental conditions (temperature, salinity, depth)  
- Range of sphere radii
- Single frequency

Results are plotted and saved as a PNG file showing TS vs sphere radius response.
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
from core.io_utils import plot_ts_vs_radius



def main():
    # User-defined parameters
    T = 10  # Temperature in °C
    S = 35  # Salinity in psu
    z = 100  # Depth in meters
    sonar_frequency = 120  # Single frequency in kHz
    radius_mm_range = np.linspace(1, 10, 50)  # Sphere radii in mm
    radii = radius_mm_range / 1000  # Convert to meters

    """
    User should modify the above parameters as needed.
    """

    # Create seawater and material objects
    water = seawater(T, z, S)
    WC = Tungsten_carbide()

    # Use ProcessPoolExecutor to parallelize radius computations
    with ProcessPoolExecutor() as executor:
        TS = list(executor.map(TS_solid_sphere, 
                                        [sonar_frequency] * len(radii),
                                        radii,
                                        [WC] * len(radii),
                                        [water] * len(radii)))

    # Convert results to numpy array and regular floats
    TS = np.array([float(ts) for ts in TS])

    """
    User can uncomment below print statements as needed
    """
    # ---------
    # print("Target Strength (dB):")
    # for i, (radius_mm, ts) in enumerate(zip(radius_mm_range, TS)):
    #   print(f"  {radius_mm:.1f} mm radius: {ts:.2f} dB")
    # ---------

    # Create plot using plot_utils
    ts_results = {"WC Sphere": TS.tolist()}
    # Save plot in the current examples directory
    current_dir = Path(__file__).parent
    plot_filename = current_dir / "WC_various_spheres_results.png"
    plot_ts_vs_radius(radius_mm_range, ts_results, sonar_frequency, labels=None, 
                     filename=plot_filename, show_plot=True, save_plot=True)
    print(f"\nPlot saved as WC_various_spheres_results.png in the examples directory")
    print("Plot window should be displayed - close it to continue.")


if __name__ == '__main__':
    main()



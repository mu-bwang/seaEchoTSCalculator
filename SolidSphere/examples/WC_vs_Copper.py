"""
Target Strength Comparison: Tungsten Carbide vs Copper Spheres

This example demonstrates how to calculate and compare the acoustic target strength (TS) 
of tungsten carbide and copper solid spheres across a range of sonar frequencies. 
The calculation uses the modal solution for elastic sphere scattering in seawater.

The script calculates TS values for both materials with user-defined parameters including:
- Environmental conditions (temperature, salinity, depth)  
- Sphere radius (same for both materials)
- Frequency range

Results are plotted and saved as a PNG file showing TS vs frequency response for comparison.
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
from utils.SeaEcho_solid_sphere import Tungsten_carbide, Copper
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
    copper = Copper()

    # Use ProcessPoolExecutor to parallelize frequency computations for both materials
    with ProcessPoolExecutor() as executor:
        # Calculate TS for Tungsten Carbide
        TS_WC = list(executor.map(TS_solid_sphere, sonar_frequencies,
                                        [radius] * len(sonar_frequencies),
                                        [WC] * len(sonar_frequencies),
                                        [water] * len(sonar_frequencies)))
        
        # Calculate TS for Copper
        TS_copper = list(executor.map(TS_solid_sphere, sonar_frequencies,
                                        [radius] * len(sonar_frequencies),
                                        [copper] * len(sonar_frequencies),
                                        [water] * len(sonar_frequencies)))

    # Convert results to numpy arrays and regular floats
    TS_WC = np.array([float(ts) for ts in TS_WC])
    TS_copper = np.array([float(ts) for ts in TS_copper])

    """
    User can uncomment below print statements as needed
    """
    # ---------
    # print("Target Strength (dB) Comparison:")
    # for i, (freq, ts_wc, ts_cu) in enumerate(zip(sonar_frequencies, TS_WC, TS_copper)):
    #   print(f"  {freq:.1f} kHz: WC = {ts_wc:.2f} dB, Copper = {ts_cu:.2f} dB, Diff = {ts_wc-ts_cu:.2f} dB")
    # ---------

    # Create plot using plot_utils - comparing both materials
    ts_results = {
        "Tungsten Carbide": TS_WC.tolist(),
        "Copper": TS_copper.tolist()
    }
    # Save plot to main project plots directory
    plot_filename = MAIN_ROOT / "plots" / "WC_vs_Copper_comparison.pdf"
    plot_ts_vs_frequency(sonar_frequencies, ts_results, radius_mm, labels=None,
                        filename=plot_filename, show_plot=True, save_plot=True)
    print(f"\nPlot saved as WC_vs_Copper_comparison.pdf in the main plots directory")
    print("Plot window should be displayed - close it to continue.")
    print(f"\nComparison Summary at {radius_mm} mm radius:")
    print(f"Frequency range: {sonar_frequencies[0]:.0f} - {sonar_frequencies[-1]:.0f} kHz")
    print(f"WC TS range: {TS_WC.min():.2f} to {TS_WC.max():.2f} dB")
    print(f"Copper TS range: {TS_copper.min():.2f} to {TS_copper.max():.2f} dB")


if __name__ == '__main__':
    main()



"""
Bubble Diameter Sweep at Fixed Frequency (18 kHz)

This script analyzes the acoustic target strength of gas bubbles with diameters
ranging from 0.2 to 6.0 mm at a fixed frequency of 18 kHz. 

Parameters:
    - Bubble diameters: 0.2 to 6.0 mm (20 steps)
    - Frequency: 18 kHz (fixed)
    - Temperature: 8.0°C
    - Salinity: 35.0 PSU
    - Depth: 500.0 m
    - Model: Medwin_Clay 

Output:
    - PNG plot: bubble_diameter_sweep_18kHz_YYYYMMDD_HHMMSS.png
    - CSV data: bubble_diameter_sweep_18kHz_YYYYMMDD_HHMMSS.csv


"""

import sys
import os
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Add the parent directories to Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.io_utils import save_figure
from core.processor import run_calculations

def main():
    """
    Calculate and plot target strength vs bubble diameter at 18 kHz.
    """

# Analysis parameters  
frequency = 18.0  # kHz - appropriate for larger bubbles (0.2-6 mm)
diameters = np.linspace(0.2e-3, 6e-3, 20)  # 0.2-6 mm, 20 points
models = ["Medwin_Clay"]  # Medwin-Clay scattering model
T = 8.0         # temperature: 8°C
S = 35.0        # salinity: 35 PSU
z = 500.0       # depth: 500 m

def main() -> None:
    """Run bubble diameter sweep analysis at fixed frequency."""
    
    # Convert to convenient units for display/calculations
    frequency_khz = frequency
    diameters_mm = diameters * 1000  # Convert to mm for display
    
    print(f"Calculating target strength vs bubble diameter at {frequency_khz} kHz...")
    print(f"Diameter range: {diameters_mm[0]:.1f} - {diameters_mm[-1]:.1f} mm ({len(diameters_mm)} points)")
    print(f"Frequency: {frequency_khz} kHz")
    print(f"Model: {models[0]}")
    print(f"Environment: {T}°C, {S} PSU, {z}m depth")
    
    # Calculate target strength for each diameter
    target_strengths = []
    
    for i, diameter_mm in enumerate(diameters_mm):
        # Parameters for this diameter using the same format as other examples
        params = {
            "frequencies": np.array([frequency_khz]),
            "d": diameter_mm * 1e-3,  # Convert mm to m  
            "models": models,
            "T": T,
            "S": S,
            "z": z,
        }
        
        # Run calculation for this diameter
        results = run_calculations(params)
        
        # Extract target strength for this diameter
        ts_value = results["results"]["ts"][models[0]][0]  # First (and only) frequency
        target_strengths.append(ts_value)
        
        if (i + 1) % 5 == 0:  # Progress indicator
            print(f"  Completed {i + 1}/{len(diameters_mm)} calculations...")
    
    # Convert to arrays for plotting
    target_strengths = np.array(target_strengths)
    
    # Debug: Print the target strength values
    print(f"\nTarget strength values:")
    for i, (d, ts) in enumerate(zip(diameters_mm, target_strengths)):
        print(f"  {d:.1f} mm: {ts:.2f} dB")
    print(f"Min TS: {np.min(target_strengths):.2f} dB")
    print(f"Max TS: {np.max(target_strengths):.2f} dB")
    print(f"Any NaN values: {np.isnan(target_strengths).any()}")
    print(f"Any infinite values: {np.isinf(target_strengths).any()}")
    
    # Create timestamp for file naming
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create the plot
    plt.figure(figsize=(6,4))
    
    # Main plot
    plt.plot(diameters_mm, target_strengths, 'b-', linewidth=2.5, marker='o', 
             markersize=6, markerfacecolor='lightblue', markeredgecolor='blue', 
             markeredgewidth=1.5)
    
    # Formatting
    plt.xlabel('Bubble Diameter (mm)', fontsize=14)
    plt.ylabel('Target Strength (dB)', fontsize=14)
    
    plt.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    
    # Set axis limits and ticks to fit data nicely
    plt.xlim(0.0, 6.2)  # Slightly beyond data range for nice appearance
    plt.ylim(-110, -35)  # Expanded to include all data from -102.74 to -38.17 dB
    plt.xticks(np.arange(0, 7, 1), fontsize=14)
    plt.yticks(fontsize=14)

    # Add model information text box (no background) - lower right corner
    info_text = (f'Frequency: {frequency_khz} kHz\n'
                f'Temperature: {T}°C\n'
                f'Salinity: {S} PSU\n'
                f'Depth: {z} m\n'
                f'Model: {models[0]}')
    
    plt.text(0.98, 0.02, info_text, transform=plt.gca().transAxes,
             fontsize=11, verticalalignment='bottom', horizontalalignment='right')
    
    plt.tight_layout()
    
    # Save plot
    plot_filename = f'bubble_diameter_sweep_{int(frequency_khz)}kHz_{timestamp}.png'
    plot_path = os.path.join('plots', plot_filename)
    os.makedirs('plots', exist_ok=True)
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    
    # Save data to CSV
    csv_filename = f'bubble_diameter_sweep_{int(frequency_khz)}kHz_{timestamp}.csv'
    csv_path = os.path.join('data', csv_filename)
    os.makedirs('data', exist_ok=True)
    
    # Create header with metadata
    header_lines = [
        f"# Bubble Target Strength vs Diameter at {frequency_khz} kHz",
        f"# Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"# Model: {models[0]}",
        f"# Frequency: {frequency_khz} kHz",
        f"# Temperature: {T}°C",
        f"# Salinity: {S} PSU", 
        f"# Depth: {z} m",
        f"# Diameter range: {diameters_mm[0]:.1f} - {diameters_mm[-1]:.1f} mm",
        f"# Number of points: {len(diameters_mm)}",
        "#",
        "Diameter_mm,Target_Strength_dB"
    ]
    
    with open(csv_path, 'w') as f:
        f.write('\n'.join(header_lines) + '\n')
        for diameter, ts in zip(diameters_mm, target_strengths):
            f.write(f'{diameter:.3f},{ts:.6f}\n')
    
    print(f"\nResults saved:")
    print(f"PNG → {plot_path}")
    print(f"CSV → {csv_path}")
    
    # Show plot
    plt.show()

if __name__ == "__main__":
    main()
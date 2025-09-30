#!/usr/bin/env python
"""
2mm_bubble_frequency_sweep.py - Bubble Target Strength Analysis

This example demonstrates bubble acoustic scattering calculations for a 2mm diameter 
air bubble across a frequency range from 1 kHz to 1200 kHz using the Modal solution 
scattering model.

WHAT THIS CODE DOES:
====================
1. Creates a 2mm diameter air bubble in seawater
2. Calculates target strength (TS) across 2000 frequency points (logarithmically spaced)
3. Uses environmental conditions: 20°C, freshwater, 10m depth
4. Applies the Modal solution scattering model (exact solution)
5. Plots TS vs frequency on a log-frequency scale
6. Exports results to CSV and PNG files with timestamps

PHYSICAL INTERPRETATION:
========================
- Target Strength (TS) represents the bubble's acoustic scattering efficiency
- Resonance peaks occur where the bubble oscillates most efficiently
- The Modal solution accounts for all scattering modes and is highly accurate
- Frequency response shows characteristic bubble resonance behavior

OUTPUT FILES:
=============
- CSV: Numerical data (frequency vs target strength)
- PNG: Visualization plot
"""

from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# Add paths for proper imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # …/Bubble
MAIN_ROOT = Path(__file__).resolve().parents[2]     # …/seaEchoTSCalculator
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(MAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(MAIN_ROOT))

# local helpers
from core.io_utils import export_results_csv, save_figure 
from core.processor import run_calculations                 

# output directories
FIG_DIR = Path(__file__).parent / "plots"
CSV_DIR = Path(__file__).parent / "data"
FIG_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)

STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")  # e.g. 20250930_154512

# Analysis parameters
params = {
    "frequencies": np.logspace(np.log10(1.0), np.log10(1200.0), 2000),  # 1-1200 kHz, 2000 points
    "d": 2e-3,                     # bubble diameter: 2 mm
    "models": ["Modal"],           # Modal solution (exact scattering model)
    "T": 20.0,                     # temperature: 20°C
    "S": 0.0,                      # salinity: 0 PSU (freshwater)
    "z": 10.0,                     # depth: 10 m
}

def main() -> None:
    """Run bubble target strength analysis and generate plots."""
    print("Calculating bubble target strength...")
    print(f"Bubble diameter: {params['d']*1000:.1f} mm")
    print(f"Frequency range: {params['frequencies'][0]:.1f} - {params['frequencies'][-1]:.1f} kHz")
    print(f"Model: {params['models'][0]}")
    print(f"Environment: {params['T']}°C, {params['S']} PSU, {params['z']}m depth")
    
    # Run calculations
    results = run_calculations(params)

    # Create improved plot
    fig, ax = plt.subplots(figsize=(6, 4))
    
    # Plot data for each model (though we only have one)
    for model_name in params["models"]:
        ax.plot(params["frequencies"], results["results"]["ts"][model_name], 
                linewidth=1.5, color='blue')

    # Customize plot with larger fonts
    ax.set_xlabel("Frequency (kHz)", fontsize=14)
    ax.set_ylabel("Target Strength (dB)", fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.set_xscale("log")
    ax.grid(True, which="both", alpha=0.3)
    
    # Add bubble information as text annotation in upper right corner
    bubble_info = f"Bubble diameter: {params['d']*1000:.1f} mm\nModel: {params['models'][0]}"
    ax.text(0.98, 0.98, bubble_info, transform=ax.transAxes, 
            verticalalignment='top', horizontalalignment='right', fontsize=12)
    
    fig.tight_layout()

    # Show plot
    plt.show()

    # Save files with descriptive names
    csv_path = CSV_DIR / f"2mm_bubble_frequency_sweep_{STAMP}.csv"
    fig_path = FIG_DIR / f"2mm_bubble_frequency_sweep_{STAMP}.png"
    
    export_results_csv(results, csv_path)
    save_figure(fig, fig_path)

    print(f"\nResults saved:")
    print(f"CSV  → {csv_path.relative_to(PROJECT_ROOT)}")
    print(f"PNG  → {fig_path.relative_to(PROJECT_ROOT)}")

if __name__ == "__main__":
    main()
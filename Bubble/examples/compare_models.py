#!/usr/bin/env python
"""
compare_models.py – Compare all available bubble-scattering models

This script performs a comprehensive comparison of all 7 bubble scattering models
available in the seaEchoTSCalculator library:

Models compared:
• Medwin_Clay: Classic bubble scattering formulation
• Breathing: Volume oscillation-focused model
• Thuraisingham: Advanced theoretical approach
• Modal: Modal analysis solution
• Weston_Medwin: Weston-Medwin formulation  
• Anderson_Weston: Anderson-Weston approach
• Ainslie_Leighton: Ainslie-Leighton model

Analysis details:
• Frequency range: 1-1200 kHz (logarithmic sweep, 2000 points)
• Single bubble: 2mm diameter in fresh water
• Environment: 20°C, 0 PSU salinity, 10m depth
• Plots Target Strength vs frequency for model comparison
• Saves timestamped PNG & CSV files (no overwrites)

Output files:
• PNG → examples/plots/compare_models_YYYYMMDD_HHMMSS.png
• CSV → examples/data/compare_models_results_YYYYMMDD_HHMMSS.csv
"""

from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # …/Bubble
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# local helpers
from core.io_utils import export_results_csv, save_figure  # noqa: E402
from core.processor import run_calculations                 # noqa: E402

# output directories
FIG_DIR = Path(__file__).parent / "plots"
CSV_DIR = Path(__file__).parent / "data"
FIG_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)

# timestamp for filenames
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# User-configurable parameters for bubble scattering analysis
params = {
    # Frequency sweep configuration (logarithmic scale)
    "frequencies": np.logspace(np.log10(1.0), np.log10(1000.0), 3000),  # 1-1000 kHz, 3000 points
    
    # Bubble characteristics
    "d": 2e-3,  # Bubble diameter in meters (2mm)
    
    # Models to compare (all 7 available models)
    "models": ["Medwin_Clay", "Breathing", "Thuraisingham", "Modal", "Weston_Medwin", "Anderson_Weston", "Ainslie_Leighton"],
    
    # Seawater environmental parameters
    "T": 20.0,  # Temperature in Celsius
    "S": 0.0,   # Salinity in PSU (0 = fresh water)
    "z": 10.0,  # Depth in meters
}

# main function to run calculations and plot results
def main() -> None:
    # run calculations
    results = run_calculations(params)

    # plot each model on same axes with compact figure size
    fig, ax = plt.subplots(figsize=(6.2, 4))
    for model in params["models"]:
        ts = results["results"]["ts"][model]
        ax.plot(params["frequencies"], ts, label=model)

    ax.set_xlabel("Frequency (kHz)", fontsize=13)
    ax.set_ylabel("Target Strength (dB)", fontsize=13)
    ax.set_xscale("log")
    ax.set_ylim(-80, 10)  # Fixed y-axis range for consistent comparison
    ax.legend(ncol=2, loc='upper right', fontsize=11)  # Two-column legend in upper right
    ax.grid(True, which="both", alpha=0.3)
    ax.tick_params(axis='both', which='major', labelsize=11)  # Increase tick label size
    fig.tight_layout()

    # Save results with timestamped filenames (prevents overwrites)
    csv_path = CSV_DIR / f"compare_models_results_{STAMP}.csv"
    fig_path = FIG_DIR / f"compare_models_{STAMP}.png"
    export_results_csv(results, csv_path)
    save_figure(fig, fig_path)

    # Display output paths relative to project root
    print(f"Results saved:")
    print(f"CSV → {csv_path.relative_to(PROJECT_ROOT)}")
    print(f"PNG → {fig_path.relative_to(PROJECT_ROOT)}")
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()

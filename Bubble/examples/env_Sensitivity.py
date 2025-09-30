#!/usr/bin/env python
"""
env_Sensitivity.py – Environmental parameter sensitivity analysis

This script analyzes how environmental conditions affect bubble scattering
by varying temperature, salinity, and depth parameters.

Analysis details:
• Model: Medwin_Clay (single model for focused environmental comparison)
• Frequency range: 1-1200 kHz (logarithmic sweep, 2000 points)
• Single bubble: 2mm diameter
• Environmental variations:
  - Temperature: 5°C, 10°C, 15°C
  - Salinity: 35 PSU (seawater)
  - Depth: 10m, 50m, 100m (varying pressure effects)

Scientific context:
• Temperature affects bubble resonance frequency and damping
• Depth (pressure) influences bubble size and compressibility
• Salinity impacts water density and sound speed
• Results show how environmental conditions shift resonance peaks

Output files:
• PNG → examples/plots/env_sensitivity_YYYYMMDD_HHMMSS.png
• CSV → examples/data/env_sensitivity_results_YYYYMMDD_HHMMSS.csv
"""

from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Project structure and imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # …/Bubble
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Local helpers and core functionality
from core.io_utils import save_figure                 # noqa: E402
from core.processor import run_calculations           # noqa: E402

# Output directories
FIG_DIR = Path(__file__).parent / "plots"
CSV_DIR = Path(__file__).parent / "data"
FIG_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)

# Timestamp for filenames
STAMP = datetime.now().strftime("%Y%m%d_%H%M%S")

# User-configurable parameters for environmental sensitivity analysis
params_config = {
    # Frequency sweep configuration (logarithmic scale)
    "frequencies": np.logspace(np.log10(1.0), np.log10(1200.0), 2000),  # 1-1200 kHz, 2000 points
    
    # Model selection (single model for focused environmental comparison)
    "models": ["Medwin_Clay"],
    
    # Bubble characteristics
    "bubble_diameter": 2e-3,  # Bubble diameter in meters (2mm)
}

# Environmental parameter variations to test
# Each dict represents one environmental condition to analyze
# Temperature decreases with depth (realistic ocean conditions)
environments = [
    {"T": 20.0, "S": 35.0, "z": 10.0},   # Warm shallow seawater
    {"T": 15.0, "S": 35.0, "z": 50.0},   # Moderate temperature, mid-depth
    {"T": 5.0,  "S": 35.0, "z": 100.0},  # Cold deep water
]

# Main function to run environmental sensitivity analysis
def main() -> None:
    # Create plot with improved styling
    fig, ax = plt.subplots(figsize=(6, 4))
    rows: list[dict] = []

    for env in environments:
        # Build parameters for this environmental condition
        params = {
            "frequencies": params_config["frequencies"],
            "d": params_config["bubble_diameter"],
            "models": params_config["models"],
            **env,  # Add T, S, z from environment dict
        }
        
        # Run calculation for this environment
        results = run_calculations(params)

        # Extract target strength values for plotting
        model_name = params_config["models"][0]
        ts_vals = results["results"]["ts"][model_name]
        label = f"T={env['T']}°C, z={env['z']}m"
        ax.plot(params_config["frequencies"], ts_vals, label=label)

        # Collect data for CSV export
        for model in params_config["models"]:
            for i, ts in enumerate(results["results"]["ts"][model]):
                rows.append({
                    "frequency_kHz": params_config["frequencies"][i],
                    "TS_dB": ts,
                    "model": model,
                    "bubble_diameter_m": params_config["bubble_diameter"],
                    "temperature_C": env['T'],
                    "salinity_PSU": env['S'],
                    "depth_m": env['z'],
                })

    # Configure plot with improved styling (consistent with other scripts)
    ax.set_xscale("log")
    ax.set_xlabel("Frequency (kHz)", fontsize=12)
    ax.set_ylabel("Target Strength (dB)", fontsize=12)
    ax.set_ylim(-80, -20)  # Adjusted y-axis range to better fit bubble scattering data
    ax.legend(title="Environment", fontsize=10, title_fontsize=11)
    ax.grid(True, which="both", alpha=0.3)
    ax.tick_params(axis='both', which='major', labelsize=10)
    fig.tight_layout()

    # Save results with timestamped filenames (prevents overwrites)
    fig_path = FIG_DIR / f"env_sensitivity_{STAMP}.png"
    csv_path = CSV_DIR / f"env_sensitivity_results_{STAMP}.csv"
    
    # Save figure
    save_figure(fig, fig_path)
    
    # Save detailed CSV with all environmental parameters
    df = pd.DataFrame(rows)
    df.to_csv(csv_path, index=False)

    # Display output paths relative to project root
    print(f"Results saved:")
    print(f"CSV → {csv_path.relative_to(PROJECT_ROOT)}")
    print(f"PNG → {fig_path.relative_to(PROJECT_ROOT)}")
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()

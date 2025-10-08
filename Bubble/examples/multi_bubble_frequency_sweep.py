#!/usr/bin/env python
"""
bubble_diameter_sweep.py - Multiple Bubble Sizes Target Strength Analysis

This example demonstrates how bubble size affects acoustic scattering by calculating 
target strength for multiple bubble diameters (0.5, 1.0, 2.0, and 5.0 mm) across 
a frequency range from 1 kHz to 1200 kHz using the Medwin-Clay scattering model.

WHAT THIS CODE DOES:
====================
1. Creates air bubbles of different diameters: 0.5, 1.0, 2.0, and 5.0 mm
2. Calculates target strength (TS) for each bubble size across 2000 frequency points
3. Uses environmental conditions: 10°C, 35 PSU salinity, 50m depth
4. Applies the Medwin-Clay scattering model (classical approximation)
5. Plots overlaid TS vs frequency curves for all bubble sizes
6. Exports combined results to CSV and PNG files with timestamps

PHYSICAL INTERPRETATION:
========================
- Different bubble sizes have different resonance frequencies
- Smaller bubbles resonate at higher frequencies
- Larger bubbles have higher target strength (more efficient scatterers)
- The Medwin-Clay model provides a practical approximation for many applications

OUTPUT FILES:
=============
- CSV: Combined data for all bubble sizes (frequency vs target strength)
- PNG: Overlay plot showing all bubble size responses
"""

from __future__ import annotations

import sys
from pathlib import Path
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ── Make project root importable ────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parents[1]   # …/Bubble
MAIN_ROOT = Path(__file__).resolve().parents[2]     # …/seaEchoTSCalculator
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(MAIN_ROOT) not in sys.path:
    sys.path.insert(0, str(MAIN_ROOT))

# local helpers
from core.io_utils import save_figure  # noqa: E402
from core.processor import run_calculations   # noqa: E402

# output directories - use main project plots and data folders
FIG_DIR = MAIN_ROOT / "plots"
CSV_DIR = MAIN_ROOT / "data"
FIG_DIR.mkdir(parents=True, exist_ok=True)
CSV_DIR.mkdir(parents=True, exist_ok=True)

# Analysis parameters
frequencies = np.logspace(np.log10(1.0), np.log10(1200.0), 2000)  # 1-1200 kHz, 2000 points
models = ["Medwin_Clay"]  # Medwin-Clay scattering model
T = 10.0        # temperature: 10°C
S = 35.0        # salinity: 35 PSU
z = 50.0        # depth: 50 m

# Bubble diameters to analyze (metres)
diameters = np.array([0.5e-3, 1e-3, 2e-3, 5e-3])  # 0.5, 1.0, 2.0, 5.0 mm

def main() -> None:
    """Run bubble diameter sweep analysis and generate plots."""
    print("Calculating target strength for multiple bubble sizes...")
    print(f"Bubble diameters: {[d*1000 for d in diameters]} mm")
    print(f"Frequency range: {frequencies[0]:.1f} - {frequencies[-1]:.1f} kHz")
    print(f"Model: {models[0]}")
    print(f"Environment: {T}°C, {S} PSU, {z}m depth")

    # Prepare improved plot
    fig, ax = plt.subplots(figsize=(6,4))
    # Collect rows for combined CSV
    rows: list[dict] = []

    for d in diameters:
        params = {
            "frequencies": frequencies,
            "d": float(d),
            "models": models,
            "T": T,
            "S": S,
            "z": z,
        }
        # Run calculation for this diameter
        results = run_calculations(params)

        # Plot TS vs frequency for this diameter
        ts_vals = results["results"]["ts"][models[0]]
        ax.plot(frequencies, ts_vals, label=f"d={d*1e3:.1f} mm")

        # Flatten results into rows
        for model in models:
            for i, ts in enumerate(results["results"]["ts"][model]):
                rows.append({
                    "frequency_kHz": frequencies[i],
                    "TS_dB": ts,
                    "model": model,
                    "bubble_diameter_m": d,
                    "temperature_C": T,
                    "salinity_PSU": S,
                    "depth_m": z,
                })

    # Customize plot with larger fonts and clean styling
    ax.set_xscale("log")
    ax.set_xlabel("Frequency (kHz)", fontsize=14)
    ax.set_ylabel("Target Strength (dB)", fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.legend(title="Diameter", fontsize=11, title_fontsize=12, loc='lower right')
    ax.grid(True, which="both", alpha=0.3)
    
    # Add model information in upper right corner
    model_info = f"Model: {models[0]}"
    ax.text(0.98, 0.98, model_info, transform=ax.transAxes, 
            verticalalignment='top', horizontalalignment='right', fontsize=12)
    
    fig.tight_layout()

    # Show plot
    plt.show()

    # Save figure with descriptive name
    fig_path = FIG_DIR / "multi_bubble_frequency_sweep.pdf"
    save_figure(fig, fig_path)

    # Save combined CSV with descriptive name
    df = pd.DataFrame(rows)
    csv_path = CSV_DIR / "multi_bubble_frequency_sweep.csv"
    df.to_csv(csv_path, index=False)

    print(f"\nResults saved:")
    print(f"PNG → {fig_path.relative_to(MAIN_ROOT)}")
    print(f"CSV → {csv_path.relative_to(MAIN_ROOT)}")

if __name__ == "__main__":
    main()
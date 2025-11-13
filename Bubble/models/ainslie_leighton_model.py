# models/ainslie_leighton_model.py

import numpy as np
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from model_specific_utils.ainslie_leighton_utils import compute_resonance_frequency, compute_damping_factors, compute_dimensionless_correction, compute_resonance_frequency_correction, compute_scattering_cross_section_AL


def calculate_ainslie_leighton_ts(f, c, water, bubble):
    """
    Compute Target Strength (TS) using the Ainslie-Leighton model.

    Parameters:
    -----------
    f : float
        Frequency in kHz.
    c : float
        Speed of sound in seawater (m/s).
    water : object
        Seawater properties.
    bubble : object
        Bubble properties.

    Returns:
    --------
    float
        Computed TS value in dB.
    """
    omega = 2 * np.pi * f * 1000  # Convert kHz to rad/s
    R_0 = bubble.d / 2  # Bubble radius

    # Compute initial resonance frequency
    omega_0_initial = compute_resonance_frequency(bubble.gamma, water.P, water.rho, R_0)

    # Compute damping factors for initial frequency
    D_thermal = bubble.K_th / (water.rho * water.cp)  # Thermal diffusivity
    beta_viscous, beta_thermal, beta_0 = compute_damping_factors(bubble.gamma, water.mu, water.rho, R_0, D_thermal)
    epsilon_0 = compute_dimensionless_correction(omega_0_initial, R_0, c)

    # Apply resonance frequency correction
    omega_0 = compute_resonance_frequency_correction(omega_0_initial, beta_0, epsilon_0)

    # Compute scattering cross-section at actual frequency
    epsilon = compute_dimensionless_correction(omega, R_0, c)
    # Recompute damping factors for actual frequency (thermal damping may be frequency dependent)
    beta_viscous_freq, beta_thermal_freq, beta_0_freq = compute_damping_factors(bubble.gamma, water.mu, water.rho, R_0, D_thermal)

    sigma_AL = compute_scattering_cross_section_AL(omega, omega_0, beta_0_freq, epsilon, R_0)

    # Compute TS
    return 10 * np.log10(sigma_AL)
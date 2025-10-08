import numpy as np
import sys
import os

# Add parent directory to path to access utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from utils.SeaEcho_acoustic_paras import resonance_freq, damping_constant

def calculate_medwin_clay_ts(f, c, water, bubble):
    """
    Compute Target Strength (TS) using the Medwin and Clay model.

    Parameters:
    -----------
    f : float
        Sonar frequency (kHz).
    c : float
        Sound speed in seawater (m/s).
    water : object
        Seawater properties, including density (rho), pressure (P), and viscosity (mu).
    bubble : object
        Bubble properties, including diameter (d), specific heat (Cp), thermal conductivity (K_th),
        adiabatic index (gamma), and gas pressure (Pg).

    Returns:
    --------
    float
        Target Strength (TS) in decibels (dB).

    Variables:
    ----------
    a : float
        Bubble radius (m), derived from diameter.
    f_b : float
        Resonance frequency without corrections (Hz).
    f_R : float
        Resonance frequency with corrections (Hz).
    correction_params : array-like
        Correction parameters [b, d/b, beta].
    delta : float
        Damping constant, including scattering, thermal, and viscous components.
    sigma_bs : float
        Backscattering cross-section (m^2).
    TS : float
        Target Strength (dB), derived from sigma_bs.
    """
    a = bubble.d / 2  # Bubble radius (m)

    # Compute resonance frequency and damping constant using existing functions
    f_b, f_R, correction_params = resonance_freq(f, c, water, bubble)
    delta = damping_constant(f, c, water, bubble)
    
    # Smart frequency selection: use f_R if valid, fallback to f_b if f_R is NaN
    if np.isnan(f_R):
        # Fallback to uncorrected frequency when corrections fail
        freq_to_use = f_b
        # Also use simplified damping when thermal corrections fail
        omega = 2 * np.pi * f * 1000  # radians/sec  
        delta_r = omega * a / c  # Re-radiation damping
        delta_nu = 4 * water.mu / (water.rho * omega * a**2)  # Viscous damping
        delta_fallback = delta_r + delta_nu  # Simplified damping
        delta_to_use = delta_fallback if np.isnan(delta) else delta
    else:
        # Use corrected frequency when available
        freq_to_use = f_R
        delta_to_use = delta
    
    # Target Strength using selected frequency and damping
    TS = 10 * np.log10(a**2 / ((freq_to_use/(f*1e3)-1)**2 + delta_to_use**2))
    return TS


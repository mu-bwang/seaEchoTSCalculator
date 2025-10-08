import numpy as np
import warnings


def resonance_freq(f, c, water, bubble):
    """
    Compute resonance frequency of bubbles with corrections.
    
    Note: correction of f_R are made for the effect of 
          surface tension and 
          thermal conductivity, See Eq. (8.2.27)

    Parameters:
    -----------
    f : float
        Sonar frequency (kHz).
    c : float
        Sound speed in seawater (m/s).
    water : object
        Seawater properties (e.g., density, pressure, etc.).
    bubble : object
        Bubble properties (e.g., radius, gas properties).
    
    Returns:
    --------
    f_b : float
        Resonance frequency (Hz) without corrections, under the assumption 
        of no surface tension, adiabatic gas oscillations, no energy absorption.
    f_R : float
        Resonance frequency (Hz) with corrections for surface tension and
        thermal conductivity.
    correction_params : numpy.ndarray
        Correction parameters [b, d/b, beta].
    """
    omega = 2 * np.pi * f * 1000    # radians/sec
    k = omega/c
    a = bubble.d/2
    
    # Check if bubble is small 
    if k*a > 1.0:
        warnings.warn("ka < 1 not satisfied!")
    
    # Calculate harmonic breathing frequency (f_b) of a small bubble (ka<<1)
    # under the assumption of no surface tension, adiabatic 
    # gas oscillations, no energy absorption. 
    # Eq(8.2.13) in Medwin and Clay (1997)
    f_b = 1/(2*np.pi*a) * np.sqrt(3 * bubble.gamma * water.P / water.rho)
    
    # Correction for the effect of surface tension and
    # thermal conductivity following Eq.(8.2.28a)-(8.2.28d), page 297
    # Note: most of parameters are in cgs
    P_in_dynes_per_cm2 = water.P * 10
    rho_g_A = bubble.rho_0*1e-3 # g/cm^3, density of free gas at sea level 
    Cpg = bubble.Cp * 0.2388 # specific heat at constant pressure of gas, convert KJ/(kg K) to cal/(g °C) 
    Kg = bubble.K_th * 0.0023900573613766683 # thermal conductivity of gas, convert W/(m K) to cal/(cm s °C), 
    tau = water.sigma * 1e3 # surface tension at gas/water interface, convert N/m to dyne/cm
    
    # Compute X with highest available precision
    X = a * 1e2 * (2*omega * rho_g_A * Cpg/Kg)**(0.5)
    
    # Use highest precision available on this system
    try:
        X = np.float128(X)  # Use float128 if available
    except AttributeError:
        try:
            X = np.longdouble(X)  # Fall back to longdouble
        except:
            X = np.float64(X)  # Fall back to float64 if necessary
    
    # Corrections for surface tension and thermal conductivity with high precision
    temporary1 = X * (np.sinh(X) + np.sin(X)) - 2 * (np.cosh(X) - np.cos(X))
    temporary2 = X**2 * (np.cosh(X) - np.cos(X)) + \
        3 * (bubble.gamma - 1) * X * (np.sinh(X) - np.sin(X))
    
    d_over_b = 3 * (bubble.gamma - 1) * temporary1 / temporary2
    
    temporary3 = (1 + d_over_b**2) * \
         (1 + (3*bubble.gamma - 3)/X * \
         ((np.sinh(X)-np.sin(X))/(np.cosh(X)-np.cos(X))))
    b = 1/temporary3
    
    beta = 1 + 2 * tau / (P_in_dynes_per_cm2 * a * 1e2) * (1-1/(3*bubble.gamma*b))
    
    # Corrected resonance frequency
    f_R = f_b * np.sqrt(b*beta)
    correction_params = np.array([b, d_over_b, beta])

    return f_b, f_R, correction_params

def damping_constant(f, c, water, bubble):
    """ 
    Compute damping constant of bubbles using Medwin and Clay (1998).

    Parameters:
    -----------
    f : float
        Sonar frequency (kHz).
    c : float
        Sound speed in seawater (m/s).
    water : object
        Seawater properties.
    bubble : object
        Bubble properties.
    
    Returns:
    --------
    float
        Total damping constant (delta).
    """
    # Convert all inputs to high precision floats
    f = np.float64(f)
    c = np.float64(c)
    omega = np.float64(2 * np.pi * f * 1000)  # Radians/sec
    a = np.float64(bubble.d / 2)

    # Compute resonance frequencies with full precision
    f_b, f_R, correction_params = resonance_freq(f, c, water, bubble)

    # Compute damping components
    delta_r = omega * a / c  # Re-radiation damping
    delta_t = correction_params[1] * (f_R / (f * 1000))**2  # Thermal damping
    delta_nu = 4 * water.mu / (water.rho * omega * a**2)  # Viscous damping

    return np.float64(delta_r + delta_t + delta_nu)


def absorption_coeff(f, water):
    """
    Calculate absorption coefficient in seawater using the simplified
    equation proposed in Ainslie and McColm (1998):
    "A simplified formula for viscous and chemical absorption in sea water"
    
    Parameters:
    -----------
    f : float or array-like
        Frequency in kHz
    water : object
        Seawater properties (requires T, S, pH, z attributes)
        
    Returns:
    --------
    alpha : float or array-like
        Absorption coefficient in dB/km
    """
    T = water.T
    S = water.S
    pH = water.pH
    z = water.z / 1000  # convert m to km
    
    f1 = 0.78 * np.sqrt(S/35.0) * np.exp(T/26.0)
    f2 = 42.0 * np.exp(T/17.0)
    
    alpha = 0.106 * (f1 * f**2)/(f**2+f1**2) * np.exp((pH-8.0)/0.56) +\
            0.52 * (1 + T/43.0) * (S/35.0) * f2 * f**2 / (f**2 + f2**2) * np.exp(-z/6.0) \
            + 0.00049 * f**2 * np.exp(-(T/27.0 + z/17.0))
            
    return alpha

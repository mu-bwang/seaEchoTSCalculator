# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 21:37:43 2023

This scipt defines a class that computes properties of bubbles in seawater


@author: wangbinb
"""

import numpy as np
from .SeaEcho_water import seawater

g = 9.81
R = 8.31446261815324 # Gas constant, (J/(mol K))


class air_bubble():
    """
    Parameters:
    --------------------------------------
           d  - bubble diameter (m)
          rho - bubble density (kg/m^3)
        rho_0 - bubble density at sea level (kg/m^3)
        gamma - specific heat ratio (-)
           Pg - pressure inside bubble (Pa)
           Mm - Molecular mass (kg/mol)
           Cp - specific heat capacity (kJ/(kg K))
         K_th - thermal conductivity (W/(m K))
         
         Note: the value of thermal conductivity is from
               Eq.7 from Stephan and Laesecke (1985):
               The Thermal Conductivity of Fluid Air
               
    """
    def __init__(self, water_class, T, z, S, diameter):
        self.water_class = water_class
        
        self.d = diameter
        self.Mm = 28.96e-3          
        self.K_th = 4.358e-3
        self.Cp = 1.005 # Note: 1.005 kJ/(kg K) = 0.24 cal/(g degC)
        self.Pg = self.pressure_and_density()[0]
        self.rho = self.pressure_and_density()[1]
        self.rho_0 = self.pressure_and_density()[2]
        self.gamma = 1.4
        
    def pressure_and_density(self):
        Pg = 1.01e5 + self.water_class.rho * g * self.water_class.z + \
                2*self.water_class.sigma/(self.d/2) - self.water_class.Pv
        # Pg = 1.01e5 + self.water_class.rho * g * self.water_class.z 
        rho = Pg * self.Mm / (R * (self.water_class.T + 273.15))
        rho_0 = 1.01e5 * self.Mm / (R * (20 + 273.15)) # 20 deg C
        return Pg, rho, rho_0

class methane_bubble():
    """
    Parameters:
    --------------------------------------
           d  - bubble diameter (m)
          rho - bubble density (kg/m^3)
        rho_0 - bubble density at sea level (kg/m^3)
        gamma - specific heat ratio (-)
           Pg - pressure inside bubble (Pa)
           Mm - Molecular mass (kg/mol)
           Cp - specific heat capacity (kJ/(kg K))
         K_th - thermal conductivity (W/(m K))
         
    Notes:
      • Values are representative for ~20–25 °C, 1 atm.
      • Cp is in kJ/(kg·K) 
      • K_th is given as an isobaric, near-ambient value (see references).

    References:
       NIST Chemistry WebBook (thermophysical properties of methane) 
       CRC Handbook of Chemistry and Physics
       NIST REFPROP/THERMPROP summaries
       Engineering Toolbox: Thermal Conductivity of Gases
       VDI Wärmeatlas / Lemmon & Jacobsen correlations
    """
    def __init__(self, water_class, T, z, S, diameter):
        self.water_class = water_class

        self.d = diameter
        self.Mm = 16.04e-3         # kg/mol (CH4)
        self.K_th = 3.40e-2        # W/(m·K) ~ 0.034 at ~25 °C
        self.Cp = 2.20             # kJ/(kg·K) (~2.19–2.23 at ~25 °C)
        self.Pg, self.rho, self.rho_0 = self.pressure_and_density()
        self.gamma = 1.31          # Cp/Cv at ~300 K

    def pressure_and_density(self):
        Pg = 1.01e5 + self.water_class.rho * g * self.water_class.z + \
                2*self.water_class.sigma/(self.d/2) - self.water_class.Pv
        rho = Pg * self.Mm / (R * (self.water_class.T + 273.15))
        rho_0 = 1.01e5 * self.Mm / (R * (20 + 273.15))  # 20 °C reference
        return Pg, rho, rho_0
class Tungsten_carbide:
    """
    Properties of Tungsten carbide solid sphere.

    Parameters (MacLennan and Dunn 1984, Foote 1990):
    -------------------------------------
    rho   - density (kg/m^3)
    c_lon - longitudinal sound speed (m/s)
    c_trans - transverse sound speed (m/s)
    """
    def __init__(self):
        self.rho = 14900
        self.c_lon = 6853
        self.c_trans = 4171

class Copper:
    """
    Properties of copper (solid, ~25 °C).

    Sources:
    - Shear & longitudinal wave speeds from Baker Hughes table (AIP Handbook + ASNT NDT Handbook). 
    - Density from EngineeringToolBox.

    rho       - density (kg/m^3)
    c_lon     - longitudinal sound speed (m/s)
    c_trans   - transverse (shear) sound speed (m/s)  [annealed]
    """
    def __init__(self):
        self.rho = 8940       # kg/m^3
        self.c_lon = 4660     # m/s  
        self.c_trans = 2325   # m/s

class Aluminum:
    """
    Properties of aluminum.

    Sources:
    - Target Strength Package V1.1 
    """
    def __init__(self):
        self.rho = 2700       # kg/m^3
        self.c_lon = 6260     # m/s  
        self.c_trans = 3080   # m/s

class Stainless_steel:
    """
    Properties of stainless steel.

    Sources:
    - Target Strength Package V1.1 
    """
    def __init__(self):
        self.rho = 7800       # kg/m^3
        self.c_lon = 5610     # m/s  
        self.c_trans = 3120   # m/s
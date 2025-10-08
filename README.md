# seaEchoTSCalculator

A comprehensive Python package for calculating acoustic target strength (TS) of gas bubbles and solid spheres in seawater, with extensive validation and visualization capabilities.

## Project Structure

```
seaEchoTSCalculator/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .gitignore                  # Git ignore rules
├── data/                       # Centralized data storage
│   ├── *_bubble_*.csv         # Bubble calculation results
│   ├── *_sphere_*.csv         # Solid sphere results
│   └── *_validation_*.csv     # Validation datasets
├── plots/                      # Centralized high-quality plots (PDF)
│   ├── *_bubble_*.pdf         # Bubble analysis plots
│   ├── *_sphere_*.pdf         # Solid sphere plots
│   ├── *_validation_*.pdf     # Validation plots
│   └── *_comparison_*.pdf     # Model comparison plots
├── validation/                 # Scientific validation notebooks
│   ├── *.ipynb               # Jupyter validation notebooks
│   ├── Case*.mat             # MATLAB reference data
│   └── *_setup.png           # Validation setup diagrams
├── tests/                      # Comprehensive test suite
│   ├── __init__.py
│   ├── test_bubble.py         # Bubble model tests
│   ├── test_solid_sphere.py   # Solid sphere tests
│   └── test_utils.py          # Utility function tests
├── Bubble/                     # Gas bubble TS calculations
│   ├── core/                  # Core functionality
│   │   ├── io_utils.py       # I/O utilities and plotting
│   │   └── processor.py      # Calculation engine
│   ├── examples/              # Example scripts
│   │   ├── *.py              # Runnable example scripts
│   │   ├── data/             # Example output data
│   │   └── plots/            # Example plots
│   ├── model_specific_utils/  # Model-specific utilities
│   │   ├── ainslie_leighton_utils.py
│   │   ├── aw_utils.py       # Anderson-Weston utilities
│   │   ├── math_utils.py     # Mathematical utilities
│   │   └── wm_utils.py       # Weston-Medwin utilities
│   └── models/               # 7 bubble TS models
│       ├── ainslie_leighton_model.py
│       ├── anderson_weston_model.py
│       ├── breathing_model.py
│       ├── medwin_clay_model.py
│       ├── modal_solution.py
│       ├── thuraisingham_model.py
│       └── weston_medwin_model.py
├── SolidSphere/               # Solid sphere TS calculations
│   ├── core/                 # Core functionality
│   │   └── io_utils.py      # I/O utilities and plotting
│   ├── examples/            # Example scripts
│   │   ├── *.py            # Runnable example scripts
│   │   ├── data/           # Example output data
│   │   └── plots/          # Example plots
│   └── models/             # Sphere TS models
│       └── SeaEcho_TS_SolidSphere.py
└── utils/                  # Common utilities and physics
    ├── SeaEcho_acoustic_paras.py    # Acoustic parameters
    ├── SeaEcho_gas_bubble.py        # Gas bubble physics
    ├── SeaEcho_solid_sphere.py      # Solid sphere materials
    └── SeaEcho_water.py             # Seawater properties
```

## Features

### Bubble Module
- **7 Validated Models**: Medwin-Clay, Breathing, Ainslie-Leighton, Anderson-Weston, Weston-Medwin, Thuraisingham, and Modal Solution
- **Environmental Parameters**: Temperature, salinity, depth, pressure, and pH effects
- **Frequency Analysis**: Calculate TS across wide frequency ranges (0.1-1000 kHz)
- **Size Analysis**: Study bubble diameter effects on TS (1-5 mm range)
- **Model Comparisons**: Side-by-side analysis of different theoretical approaches
- **Environmental Sensitivity**: Analyze effects of oceanic conditions

### SolidSphere Module  
- **Material Support**: Tungsten Carbide, Copper, and extensible framework for other materials
- **Frequency Analysis**: TS calculations across acoustic frequency ranges
- **Size Comparisons**: Multiple sphere radii analysis
- **Material Comparisons**: Side-by-side TS analysis for different materials
- **High-Precision Calculations**: Using arbitrary-precision mathematics for accuracy

### Validation Suite
- **8 Jupyter Notebooks**: Comprehensive scientific validation against literature
- **Reference Comparisons**: Weber et al. (2014), Ainslie & McColm (1998), Medwin & Clay (1998)
- **Physics Validation**: Absorption coefficients, resonance frequencies, damping constants
- **Environmental Models**: Seawater density and acoustic parameter validation
- **Interactive Analysis**: Bubble ka-analysis and high-frequency model comparisons

## Installation

### Requirements
- Python ≥3.8
- NumPy ≥1.26.0 (numerical computations)
- MPmath ≥1.3.0 (arbitrary-precision mathematics)
- Matplotlib ≥3.8.0 (plotting and visualization)
- Pandas ≥2.2.0 (data handling and CSV export)

### Step-by-Step Setup
```bash
# Clone repository
git clone https://github.com/sbsLabib/seaEchoTSCalculator
cd seaEchoTSCalculator

# Create virtual environment
python -m venv .venv
source .venv/bin/activate      # Linux/Mac
.\.venv\Scripts\activate       # Windows

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

### Running Examples

#### Bubble Examples
```bash
cd Bubble/examples
python 2mm_bubble_frequency_sweep.py          # Single bubble frequency analysis
python diameter_sweep_18kHz.py                # Bubble size effects at 18 kHz
python compare_models.py                      # Compare all 7 bubble models
python env_Sensitivity.py                     # Environmental parameter effects
python multi_bubble_frequency_sweep.py        # Multiple bubble size analysis
```

#### SolidSphere Examples
```bash
cd SolidSphere/examples
python Single_sphere_across_freq_range.py     # Single sphere frequency analysis
python various_radius_for_same_freq.py        # Multiple sphere sizes
python WC_vs_Copper.py                        # Material comparison analysis
```

#### Validation Notebooks
```bash
# Launch Jupyter and open validation notebooks
jupyter notebook validation/
# Available notebooks:
# - bubble_target_strength_validation.ipynb    # Weber et al. (2014) validation
# - absorption_coefficient_validation.ipynb    # Ainslie & McColm (1998) validation
# - medwin_clay_validation.ipynb              # Medwin & Clay (1998) validation
# - seawater_density_validation.ipynb         # Seawater physics validation
# - high_frequency_validation.ipynb           # High-frequency model comparison
# - bubble_1mm_ka_analysis.ipynb             # Dimensionless analysis
# - wc_sphere_*mm_validation.ipynb           # Solid sphere validation
```

## Output Structure

All outputs are centrally organized:

### Data Files (`/data/`)
- **CSV format** with timestamped results
- Comprehensive calculation metadata
- Ready for further analysis or plotting

### Plots (`/plots/`)
- **Publication-quality PDF files** (300 DPI)
- Professional styling with 12pt fonts
- Consistent formatting across all outputs
- 6×4 inch format optimized for publications

### Example Outputs
- **Bubble examples**: Individual `data/` and `plots/` subdirectories
- **SolidSphere examples**: Individual `data/` and `plots/` subdirectories
- **Validation**: Results saved to main `/data/` and `/plots/` directories

## Validation & Scientific Accuracy

### Comprehensive Validation Suite
The package includes extensive validation against peer-reviewed literature:

- **Weber et al. (2014)**: Bubble target strength in Gulf of Mexico conditions
- **Ainslie & McColm (1998)**: Seawater absorption coefficient validation
- **Medwin & Clay (1998)**: Resonance frequency and damping validation
- **High-frequency analysis**: Model comparison across frequency ranges
- **Seawater physics**: Density and acoustic parameter validation

### Model Verification
- 7 independent bubble scattering models
- Cross-validation between analytical and numerical approaches
- Dimensionless analysis (ka parameter studies)
- Environmental parameter sensitivity analysis

## Testing

Run the comprehensive test suite from the project root:
```bash
python -m pytest tests/                       # Run all tests
python tests/test_bubble.py                   # Bubble-specific tests
python tests/test_solid_sphere.py             # Solid sphere tests
python tests/test_utils.py                    # Utility function tests
```

## Dependencies & Architecture

### Core Dependencies
- **NumPy**: Numerical computations and array operations
- **MPmath**: Arbitrary-precision mathematics for solid sphere calculations
- **Matplotlib**: Professional-quality plotting and visualization  
- **Pandas**: Data handling, CSV export, and analysis

### Modular Architecture
- **Centralized utilities**: Common physics models in `/utils/`
- **Specialized modules**: Separate `Bubble/` and `SolidSphere/` implementations
- **Consistent I/O**: Standardized plotting and data export across modules
- **Validation-driven**: Scientific accuracy verified through extensive validation
- **Publication-ready**: All outputs formatted for scientific publication

## Scientific Applications

### Oceanographic Research
- Methane bubble detection and quantification
- Underwater acoustic scattering analysis
- Environmental monitoring applications

### Sonar and Acoustics
- Target strength predictions for detection systems
- Acoustic scattering cross-section calculations
- Multi-frequency analysis capabilities

### Material Science
- Solid sphere scattering for material characterization
- Acoustic property determination
- Comparative material analysis

## Documentation & Usage

### Interactive Documentation
- **Jupyter notebooks**: Step-by-step validation and analysis
- **Example scripts**: Ready-to-run demonstrations
- **Inline documentation**: Comprehensive docstrings and comments

### Scientific References
All models implemented based on peer-reviewed literature with full citation tracking and validation against original publications.

## Contributing

The project follows scientific software development best practices:
- Modular design with clear separation of concerns
- Comprehensive testing and validation
- Consistent coding standards and documentation
- Version-controlled development with Git
- Publication-quality output standards

---

**Note**: All calculations validated against peer-reviewed literature. See validation notebooks for detailed comparisons and scientific accuracy verification.

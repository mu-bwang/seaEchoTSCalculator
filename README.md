# seaEchoTSCalculator

A Python package for calculating acoustic target strength (TS) of gas bubbles and solid spheres in seawater.

## Project Structure

```
seaEchoTSCalculator/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── tests/                   # Centralized test files
│   ├── __init__.py
│   ├── test_bubble.py
│   ├── test_solid_sphere.py
│   └── test_utils.py
├── Bubble/                  # Gas bubble TS calculations
│   ├── core/               # Core functionality
│   │   ├── io_utils.py    # I/O utilities
│   │   └── processor.py   # Calculation engine
│   ├── examples/          # Example scripts and results
│   ├── model_specific_utils/  # Model-specific utilities
│   └── models/            # Bubble TS models
├── SolidSphere/            # Solid sphere TS calculations
│   ├── core/              # Core functionality
│   │   └── io_utils.py   # I/O utilities and plotting
│   ├── examples/         # Example scripts and results
│   └── models/           # Sphere TS models
└── utils/                 # Common utilities
    ├── SeaEcho_bubble_resonance.py
    ├── SeaEcho_gas_bubble.py
    ├── SeaEcho_solid_sphere.py
    └── SeaEcho_water.py
```

## Features

### Bubble Module
- **7 Different Models**: Medwin-Clay, Breathing, Ainslie-Leighton, Anderson-Weston, Weston-Medwin, Thuraisingham, and Modal Solution
- **Environmental Parameters**: Temperature, salinity, depth, pressure effects
- **Frequency Sweeps**: Calculate TS across frequency ranges
- **Diameter Analysis**: Study bubble size effects on TS

### SolidSphere Module  
- **Material Support**: Tungsten Carbide, Copper, and extensible to other materials
- **Frequency Analysis**: TS calculations across acoustic frequency ranges
- **Size Comparisons**: Multiple sphere radii analysis
- **Material Comparisons**: Side-by-side TS analysis

## Installation

### Requirements
- Python ≥3.8

### Step-by-Step Setup
```bash
# Clone repository
git clone https://github.com/sbsLabib/seaEchoTSCalculator
cd seaEchoTSCalculator

# Create virtual environment
python -m venv ts-env
source ts-env/bin/activate  # Linux/Mac
.\ts-env\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```
## Quick Start

### Running Examples

#### Bubble Examples
```bash
cd Bubble/examples
python 2mm_bubble_frequency_sweep.py
python diameter_sweep_18kHz.py
python compare_models.py
python env_Sensitivity.py
python multi_bubble_frequency_sweep.py
```

#### SolidSphere Examples
```bash
cd SolidSphere/examples
python Single_sphere_across_freq_range.py
python various_radius_for_same_freq.py
python WC_vs_Copper.py
```

## Output

All examples generate:
- **Timestamped CSV files** with calculation results in `examples/data/`
- **Publication-quality plots** saved as PNG files in `examples/`
- **Console output** with summary statistics

Plot format: 6×4 inches, 12pt fonts, professional styling for publications.

## Testing

Run the test suite from the project root:
```bash
python tests/test_bubble.py
python tests/test_solid_sphere.py
python tests/test_utils.py
```

## Dependencies

- NumPy: Numerical computations
- Matplotlib: Plotting and visualization  
- Pandas: Data handling and CSV export
- MPmath: Arbitrary-precision mathematics

## Documentation

For detailed usage instructions, see:
- Example scripts in each module's `examples/` directory
- Inline code documentation and docstrings
- Test files in `tests/` directory for usage examples

## Contributing

The project follows a modular structure with:
- Consistent import patterns using relative imports
- Standardized I/O utilities in each module's `core/` directory
- Centralized testing in `tests/` directory
- Professional plotting standards across all outputs

---

All documentation is centralized in this README file.

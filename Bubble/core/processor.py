# core/processor.py
import sys
import os
import numpy as np
from concurrent.futures import ProcessPoolExecutor
from functools import partial  

# Add parent directory to path to access utils - go up from Bubble/core to root
current_file = os.path.abspath(__file__)
bubble_core_dir = os.path.dirname(current_file)  # Bubble/core
bubble_dir = os.path.dirname(bubble_core_dir)    # Bubble
root_dir = os.path.dirname(bubble_dir)           # seaEchoTSCalculator

# Add root directory to path
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from utils.SeaEcho_water import seawater
from utils.SeaEcho_gas_bubble import air_bubble


# Model imports - add Bubble directory to path for model imports
if bubble_dir not in sys.path:
    sys.path.insert(0, bubble_dir)

from models.medwin_clay_model import calculate_medwin_clay_ts
from models.breathing_model import calculate_breathing_ts
from models.thuraisingham_model import calculate_thuraisingham_ts
from models.modal_solution import calculate_modal_ts
from models.wildt_medwin_model import calculate_wm_ts
from models.andreeva_weston_model import calculate_aw_ts
from models.ainslie_leighton_model import calculate_ainslie_leighton_ts

MODEL_FUNCTIONS = {
    "Medwin_Clay": calculate_medwin_clay_ts,
    "Breathing": calculate_breathing_ts,
    "Thuraisingham": calculate_thuraisingham_ts,
    "Modal": calculate_modal_ts,
    "Wildt_Medwin": calculate_wm_ts,
    "Andreeva_Weston": calculate_aw_ts,
    "Ainslie_Leighton": calculate_ainslie_leighton_ts
}

def _process_wrapper(f, water_params, bubble_params, c, models):
    """Reconstruct objects using positional arguments"""
    # Recreate seawater from tuple (T, z, S)
    water = seawater(*water_params)
    
    # Recreate bubble using (water, T, z, S, d)
    bubble = air_bubble(water, *bubble_params)
    
    return _process_single_frequency(f, water, bubble, c, models)

def _process_single_frequency(f, water, bubble, c, models):
    """Core TS calculation logic"""
    k = 2 * np.pi * f * 1000 / c
    a = bubble.d / 2
    ka = k * a
    
    ts_values = {"ka": ka}
    for model in models:
        ts_values[model] = MODEL_FUNCTIONS[model](f, c, water, bubble)
    
    return ts_values

def run_calculations(params):
    """Parallel execution coordinator"""
    # Initialize objects (unchanged)
    water = seawater(params['T'], params['z'], params['S'])
    bubble = air_bubble(water, params['T'], params['z'], params['S'], params['d'])
    c = water.c
    
    # Prepare parameters as tuples for positional arguments
    water_params = (params['T'], params['z'], params['S'])
    bubble_params = (params['T'], params['z'], params['S'], params['d'])
    
    # Create partial function
    processor = partial(
        _process_wrapper,
        water_params=water_params,
        bubble_params=bubble_params,
        c=c,
        models=params['models']
    )
    
    # Execute in parallel
    with ProcessPoolExecutor() as executor:
        results = list(executor.map(processor, params['frequencies']))
    
    # Organize results into dictionary format
    processed = {
        'ka': np.array([res['ka'] for res in results]),
        'ts': {model: np.array([res[model] for res in results]) 
               for model in params['models']}
    }
    
    return {
        'params': params,
        'results': processed,  # Now a DICT with 'ka' and 'ts' keys
        'environment': {'water': water, 'bubble': bubble, 'c': c}
    }
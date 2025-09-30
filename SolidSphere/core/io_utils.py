# SolidSphere/core/io_utils.py
from pathlib import Path
import matplotlib.pyplot as plt


def save_figure(fig, outpath: Path) -> None:
    """
    Save a matplotlib figure `fig` to `outpath`, creating directories as needed.
    """
    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, dpi=300, bbox_inches="tight")


def plot_ts_vs_frequency(frequencies, ts_results, radius_mm, labels=None,
                         filename="TS_vs_frequency_sphere.png", show_plot=True, save_plot=True):
    """
    Plot Target Strength results versus frequency on a linear x-axis.
    
    Parameters:
    -----------
    frequencies : array-like
        Frequency values in kHz
    ts_results : dict
        Dictionary with model names as keys and TS values as values
    radius_mm : float
        Sphere radius in mm (for title display)
    labels : list or None
        Labels for the plot (currently not used)
    filename : str
        Filename for saving the plot (only used if save_plot=True)
    show_plot : bool
        Whether to display the plot window (default: True)
    save_plot : bool
        Whether to save the plot to file (default: True)
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    
    for model, ts_values in ts_results.items():
        ax.plot(frequencies, ts_values, label=model)
    
    ax.set_xlabel("Frequency (kHz)", fontsize=12)
    ax.set_ylabel("Target Strength, TS (dB)", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(which="both", linestyle="--", linewidth=0.5)
    
    plt.tight_layout()

    # Save the plot if requested
    if save_plot:
        if isinstance(filename, str):
            # Convert to Path relative to SolidSphere directory
            base_dir = Path(__file__).parent.parent
            save_path = base_dir / filename
        else:
            save_path = Path(filename)
        save_figure(fig, save_path)
    
    # Show the plot if requested
    if show_plot:
        plt.show()
    
    plt.close(fig)


def plot_ts_vs_radius(radii_mm, ts_results, frequency_khz, labels=None,
                      filename="TS_vs_radius_sphere.png", show_plot=True, save_plot=True):
    """
    Plot Target Strength results versus sphere radius at a fixed frequency.
    
    Parameters:
    -----------
    radii_mm : array-like
        Sphere radii values in mm
    ts_results : dict
        Dictionary with model names as keys and TS values as values
    frequency_khz : float
        The frequency in kHz used for the calculations
    labels : list or None
        Labels for the plot (currently not used)
    filename : str
        Filename for saving the plot (only used if save_plot=True)
    show_plot : bool
        Whether to display the plot window (default: True)
    save_plot : bool
        Whether to save the plot to file (default: True)
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    
    for model, ts_values in ts_results.items():
        ax.plot(radii_mm, ts_values, label=model, linewidth=2)
    
    ax.set_xlabel("Sphere Radius (mm)", fontsize=12)
    ax.set_ylabel("Target Strength, TS (dB)", fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(which="both", linestyle="--", linewidth=0.5)
    
    plt.tight_layout()

    # Save the plot if requested
    if save_plot:
        if isinstance(filename, str):
            # Convert to Path relative to SolidSphere directory
            base_dir = Path(__file__).parent.parent
            save_path = base_dir / filename
        else:
            save_path = Path(filename)
        save_figure(fig, save_path)
    
    # Show the plot if requested
    if show_plot:
        plt.show()
    
    plt.close(fig)
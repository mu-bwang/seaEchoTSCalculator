# examples/utils.py
from pathlib import Path
import pandas as pd
def export_results_csv(results: dict, outpath: Path) -> None:
    """
    Flatten the `results` dict from `run_calculations` into a long-form
    DataFrame and write it to disk at `outpath`.
    """
    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)

    freqs = results["params"]["frequencies"]
    rows = []
    for model, ts_vals in results["results"]["ts"].items():
        for i, ts in enumerate(ts_vals):
            row = {
                "frequency_kHz": freqs[i],
                "TS_dB": ts,
                "model": model,
                # include bubble diameter
                "bubble_diameter_m": results["params"].get("bubble_diameter")
            }
            # include environment fields if present (dataclass or dict)
            env = results["params"].get("environment")
            if env is not None:
                if hasattr(env, "__dict__"):
                    row.update(env.__dict__)
                elif isinstance(env, dict):
                    row.update(env)
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(outpath, index=False)


def save_figure(fig, outpath: Path) -> None:
    """
    Save a matplotlib figure `fig` to `outpath`, creating directories as needed.
    """
    outpath = Path(outpath)
    outpath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(outpath, dpi=300, bbox_inches="tight")

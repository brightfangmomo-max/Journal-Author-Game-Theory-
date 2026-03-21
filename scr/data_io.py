"""
data_io.py — shared utilities for saving/loading computed figure data as JSON.

Usage in figure scripts:
    from data_io import save_data, load_data, DATA_DIR

Numpy arrays are serialised as {"__ndarray__": true, "data": [...], "dtype": "float64"}.
"""

import json
import os
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')


class _NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return {"__ndarray__": True, "data": obj.tolist(), "dtype": str(obj.dtype)}
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)


def _np_hook(d):
    if "__ndarray__" in d:
        return np.array(d["data"], dtype=d["dtype"])
    return d


def save_data(data, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        json.dump(data, f, cls=_NpEncoder, indent=2, allow_nan=True)


def load_data(path):
    with open(path) as f:
        return json.load(f, object_hook=_np_hook)

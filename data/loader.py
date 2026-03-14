import pandas as pd
from pathlib import Path

def load_csv_files(paths):
    """
    Devuelve un dict:
    {
        "archivo.csv": DataFrame,
        ...
    }
    """
    data = {}

    for path in paths:
        name = Path(path).stem   # nombre sin .csv
        df = pd.read_csv(path)
        data[name] = df

    return data


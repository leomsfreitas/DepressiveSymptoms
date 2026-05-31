import pandas as pd

def load_features(base_path: str, *feature_paths: str, key: str = "DOCNO") -> pd.DataFrame:
    df = pd.read_csv(base_path)
    for path in feature_paths:
        df = df.merge(pd.read_csv(path), on=key)
    return df
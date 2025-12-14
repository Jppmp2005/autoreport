import pandas as pd

def analyze_csv(path):
    df = pd.read_csv(path)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    stats = {}
    for col in numeric_cols:
        stats[col] = {
            "mean": float(df[col].mean()),
            "min": float(df[col].min()),
            "max": float(df[col].max()),
            "count": int(df[col].count())
        }

    return df.head(20), stats, numeric_cols

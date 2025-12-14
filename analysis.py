import pandas as pd

def analyze_csv(path):
    """
    Lê um CSV e retorna:
    - preview: primeiras 20 linhas
    - stats: estatísticas de colunas numéricas (mean, min, max, count)
    - numeric_cols: lista de colunas numéricas
    """
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

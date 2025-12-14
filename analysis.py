import pandas as pd

def analyze_csv(path):
    """
    Lê o CSV e retorna:
    - preview das primeiras 20 linhas
    - stats por coluna numérica, incluindo Total_Faltas
    - lista de colunas numéricas (numeric_cols)
    - insights automáticos por funcionário
    """
    df = pd.read_csv(path)

    # Seleciona colunas numéricas
    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # Estatísticas básicas por coluna
    stats = {}
    for col in numeric_cols:
        stats[col] = {
            "total": int(df[col].sum()),
            "media": round(float(df[col].mean()), 2),
            "max": int(df[col].max()),
            "min": int(df[col].min())
        }

    # Total de faltas por funcionário
    df["Total_Faltas"] = df[numeric_cols].sum(axis=1)

    # Adiciona Total_Faltas ao stats
    stats["Total_Faltas"] = {
        "total": int(df["Total_Faltas"].sum()),
        "media": round(float(df["Total_Faltas"].mean()), 2),
        "max": int(df["Total_Faltas"].max()),
        "min": int(df["Total_Faltas"].min())
    }

    numeric_cols.append("Total_Faltas")

    # Insights simples
    insights = []
    media_total = df["Total_Faltas"].mean()
    for _, row in df.iterrows():
        if row["Total_Faltas"] > media_total:
            insights.append(f"{row['Nome']} teve {row['Total_Faltas']} faltas, acima da média do grupo.")
        else:
            insights.append(f"{row['Nome']} teve {row['Total_Faltas']} faltas, dentro da média.")

    return df.head(20), stats, numeric_cols, insights



import pandas as pd

def analyze_csv(path):
    """
    Lê CSV e retorna:
    - preview das primeiras 20 linhas
    - stats de cada coluna numérica
    - insights por funcionário
    """
    df = pd.read_csv(path)

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    # Estatísticas básicas
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
    if "Total_Faltas" not in numeric_cols:
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


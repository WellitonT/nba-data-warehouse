import pandas as pd


def remover_linhas_totais(df: pd.DataFrame) -> pd.DataFrame:
    return df[df["TEAM_ABBREVIATION"] != "TOT"]

def corrigir_tipos_numericos(df: pd.DataFrame) -> pd.DataFrame:
    colunas_numericas = [
        "PLAYER_AGE", "GP", "GS", "MIN", "FGM", "FGA", "FG_PCT",
        "FG3M", "FG3A", "FG3_PCT", "FTM", "FTA", "FT_PCT",
        "OREB", "DREB", "REB", "AST", "STL", "BLK", "TOV",
        "PF", "PTS"
    ]

    df = df.copy()
    for coluna in colunas_numericas:
        df[coluna] = pd.to_numeric(df[coluna])
    return df

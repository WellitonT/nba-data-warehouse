import pandas as pd
from src.transform.limpeza import remover_linhas_totais

def test_remove_linhas_totais():
    dados = pd.DataFrame({
        "TEAM_ABBREVIATION": ["LAC", "CLE", "TOT"],
        "PTS": [1118, 534, 1652]
    })

    resultado = remover_linhas_totais(dados)

    assert len(resultado) == 2
    assert "TOT" not in resultado["TEAM_ABBREVIATION"].values
import os
import pandas as pd
from src.load.database import criar_banco, inserir_estatisticas
from src.models.estatistica_temporada import EstatisticaTemporada
import sqlite3

def test_nao_duplica_ao_inserir_duas_vezes():
    caminho_teste = "data/teste_banco.db"

    if os.path.exists(caminho_teste):
        os.remove(caminho_teste)

    estatistica = EstatisticaTemporada(
        player_id="123", season_id="2025-26", team_id="997",
        team_abbreviation="TST", idade=25.0, jogos_disputados=10,
        minutos=200, pontos=100, rebotes=50, assistencias=30,
        roubos=5, bloqueios=2,
    )

    df_elenco_falso = pd.DataFrame({
        "PLAYER_ID": ["123"],
        "PLAYER": ["Jogador Teste"],
    })

    criar_banco(caminho_banco=caminho_teste)
    inserir_estatisticas([estatistica], df_elenco_falso, caminho_banco=caminho_teste)
    inserir_estatisticas([estatistica], df_elenco_falso, caminho_banco=caminho_teste) # De propósito duas vezes

    conexao = sqlite3.connect(caminho_teste)
    resultado = conexao.execute("SELECT COUNT(*) FROM fato_estatisticas_temporada").fetchone()
    conexao.close()

    assert resultado[0] == 1
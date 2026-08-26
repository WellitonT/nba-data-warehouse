import sqlite3
from src.load.database import CAMINHO_BANCO


def top_pontuadores(caminho_banco=CAMINHO_BANCO, limite: int = 5) -> list:
    query = """
        SELECT dim_jogador.nome, SUM(fato_estatisticas_temporada.pontos) AS total_pontos
        FROM fato_estatisticas_temporada
        JOIN dim_jogador ON fato_estatisticas_temporada.player_id = dim_jogador.player_id
        GROUP BY dim_jogador.nome
        ORDER BY total_pontos DESC
        LIMIT ?
    """
    conexao = sqlite3.connect(caminho_banco)
    resultado = conexao.execute(query, (limite,)).fetchall()
    conexao.close()
    return resultado
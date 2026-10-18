import sqlite3
from contextlib import closing

from src.load.database import CAMINHO_BANCO

# Nomes de coluna não podem ser parâmetros (?) em SQL. Quando a coluna vem de
# fora (UI), a única defesa é uma lista fechada. Nunca interpole sem validar.
METRICAS_PERMITIDAS = ("pontos", "rebotes", "assistencias", "roubos", "bloqueios")
TABELAS_DO_WAREHOUSE = ("dim_jogador", "dim_time", "fato_estatisticas_temporada")


def _validar_metrica(metrica: str) -> str:
    if metrica not in METRICAS_PERMITIDAS:
        raise ValueError(f"Métrica inválida: {metrica!r}. Use uma de {METRICAS_PERMITIDAS}")
    return metrica


def top_pontuadores(caminho_banco=CAMINHO_BANCO, limite: int = 5) -> list:
    query = """
        SELECT dim_jogador.nome, SUM(fato_estatisticas_temporada.pontos) AS total_pontos
        FROM fato_estatisticas_temporada
        JOIN dim_jogador ON fato_estatisticas_temporada.player_id = dim_jogador.player_id
        GROUP BY dim_jogador.player_id, dim_jogador.nome
        ORDER BY total_pontos DESC
        LIMIT ?
    """
    with closing(sqlite3.connect(caminho_banco)) as conexao:
        return conexao.execute(query, (limite,)).fetchall()


def listar_temporadas(caminho_banco=CAMINHO_BANCO) -> list[str]:
    query = "SELECT DISTINCT season_id FROM fato_estatisticas_temporada ORDER BY season_id DESC"
    with closing(sqlite3.connect(caminho_banco)) as conexao:
        return [linha[0] for linha in conexao.execute(query).fetchall()]


def top_jogadores(
    metrica: str,
    season_id: str,
    limite: int = 10,
    caminho_banco=CAMINHO_BANCO,
) -> list[tuple[str, int]]:
    coluna = _validar_metrica(metrica)
    query = f"""
        SELECT j.nome, SUM(f.{coluna}) AS total
        FROM fato_estatisticas_temporada AS f
        JOIN dim_jogador AS j ON f.player_id = j.player_id
        WHERE f.season_id = ?
        GROUP BY j.player_id, j.nome
        ORDER BY total DESC
        LIMIT ?
    """
    with closing(sqlite3.connect(caminho_banco)) as conexao:
        return conexao.execute(query, (season_id, limite)).fetchall()


def total_por_time(
    metrica: str,
    season_id: str,
    caminho_banco=CAMINHO_BANCO,
) -> list[tuple[str, int]]:
    coluna = _validar_metrica(metrica)
    query = f"""
        SELECT t.sigla, SUM(f.{coluna}) AS total
        FROM fato_estatisticas_temporada AS f
        JOIN dim_time AS t ON f.team_id = t.team_id
        WHERE f.season_id = ?
        GROUP BY t.team_id, t.sigla
        ORDER BY total DESC
    """
    with closing(sqlite3.connect(caminho_banco)) as conexao:
        return conexao.execute(query, (season_id,)).fetchall()


def contagem_por_tabela(caminho_banco=CAMINHO_BANCO) -> dict[str, int]:
    with closing(sqlite3.connect(caminho_banco)) as conexao:
        return {
            tabela: conexao.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
            for tabela in TABELAS_DO_WAREHOUSE
        }
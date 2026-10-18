import sqlite3

import pytest

from src.analytics.consultas import (
    contagem_por_tabela,
    listar_temporadas,
    top_jogadores,
    top_pontuadores,
    total_por_time,
)

# Se você já tem um helper que cria o schema nos testes de database.py,
# use ele aqui no lugar deste DDL e apague a duplicação.
DDL = """
CREATE TABLE dim_jogador (player_id TEXT PRIMARY KEY, nome TEXT NOT NULL);
CREATE TABLE dim_time (team_id TEXT PRIMARY KEY, sigla TEXT NOT NULL);
CREATE TABLE fato_estatisticas_temporada (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id TEXT NOT NULL, team_id TEXT NOT NULL, season_id TEXT NOT NULL,
    idade REAL, jogos_disputados INTEGER, minutos INTEGER,
    pontos INTEGER, rebotes INTEGER, assistencias INTEGER,
    roubos INTEGER, bloqueios INTEGER,
    UNIQUE (player_id, team_id, season_id)
);
"""


@pytest.fixture
def banco(tmp_path):
    caminho = tmp_path / "teste.db"
    conexao = sqlite3.connect(caminho)
    conexao.executescript(DDL)
    conexao.executemany(
        "INSERT INTO dim_jogador VALUES (?, ?)",
        [("1", "Ana Silva"), ("2", "Bruno Costa"), ("3", "Ana Silva")],  # homônimos: 1 e 3
    )
    conexao.executemany(
        "INSERT INTO dim_time VALUES (?, ?)", [("10", "AAA"), ("20", "BBB")]
    )
    conexao.executemany(
        "INSERT INTO fato_estatisticas_temporada "
        "(player_id, team_id, season_id, pontos, rebotes, assistencias, roubos, bloqueios) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [
            ("1", "10", "2024-25", 100, 50, 10, 5, 2),
            ("2", "20", "2024-25", 300, 20, 80, 9, 1),
            ("3", "20", "2024-25", 200, 70, 30, 4, 8),
            ("2", "20", "2023-24", 999, 1, 1, 1, 1),
        ],
    )
    conexao.commit()
    conexao.close()
    return caminho


def test_top_pontuadores_nao_funde_homonimos(banco):
    resultado = top_pontuadores(caminho_banco=banco, limite=10)
    nomes = [nome for nome, _ in resultado]
    assert nomes.count("Ana Silva") == 2


def test_top_jogadores_filtra_temporada_e_ordena(banco):
    resultado = top_jogadores("pontos", "2024-25", limite=2, caminho_banco=banco)
    assert resultado == [("Bruno Costa", 300), ("Ana Silva", 200)]


def test_top_jogadores_rejeita_metrica_fora_da_whitelist(banco):
    with pytest.raises(ValueError):
        top_jogadores("pontos; DROP TABLE dim_jogador", "2024-25", caminho_banco=banco)


def test_total_por_time_agrega_por_sigla(banco):
    resultado = total_por_time("rebotes", "2024-25", caminho_banco=banco)
    assert resultado == [("BBB", 90), ("AAA", 50)]


def test_listar_temporadas_ordem_decrescente(banco):
    assert listar_temporadas(banco) == ["2024-25", "2023-24"]


def test_contagem_por_tabela(banco):
    contagem = contagem_por_tabela(banco)
    assert contagem == {
        "dim_jogador": 3,
        "dim_time": 2,
        "fato_estatisticas_temporada": 4,
    }
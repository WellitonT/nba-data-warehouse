import sqlite3
from pathlib import Path

CAMINHO_BANCO = Path("data") / "nba_warehouse.db"
CAMINHO_SCHEMA = Path("sql") / "ddl" / "schema.sql"

def criar_banco() -> None:
    with open(CAMINHO_SCHEMA, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.executescript(schema_sql)
    conexao.commit()
    conexao.close()

def inserir_estatisticas(lista_estatisticas: list, df_elenco) -> None:
    conexao = sqlite3.connect(CAMINHO_BANCO)
    cursor = conexao.cursor()

    # Monta um dicionário player_id -> nome, a partir do elenco
    nomes_por_id = dict(zip(df_elenco["PLAYER_ID"], df_elenco["PLAYER"]))

    for estatistica in lista_estatisticas:
        nome_jogador = nomes_por_id.get(estatistica.player_id, "Desconhecido")

        cursor.execute(
            "INSERT OR IGNORE INTO dim_jogador (player_id, nome) VALUES (? ,?)",
            (estatistica.player_id, nome_jogador)
        )
        cursor.execute(
            "INSERT OR IGNORE INTO dim_time (team_id, sigla) VALUES (?, ?)",
            (estatistica.team_id, estatistica.team_abbreviation)
        )
        cursor.execute(
            """INSERT OR IGNORE INTO fato_estatisticas_temporada
            (player_id, team_id, season_id, idade, jogos_disputados, minutos,
            pontos, rebotes, assistencias, roubos, bloqueios)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (estatistica.player_id, estatistica.team_id, estatistica.season_id,
             estatistica.idade, estatistica.jogos_disputados, estatistica.minutos,
             estatistica.pontos, estatistica.rebotes, estatistica.assistencias,
             estatistica.roubos, estatistica.bloqueios)
        )

    conexao.commit()
    conexao.close()



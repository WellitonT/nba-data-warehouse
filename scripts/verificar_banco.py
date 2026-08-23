import sqlite3
from src.load.database import CAMINHO_BANCO

conexao = sqlite3.connect(CAMINHO_BANCO)
print(conexao.execute("SELECT COUNT(*) FROM dim_jogador").fetchone())
print(conexao.execute("SELECT COUNT(*) FROM dim_time").fetchone())
print(conexao.execute("SELECT COUNT(*) FROM fato_estatisticas_temporada").fetchone())
conexao.close()
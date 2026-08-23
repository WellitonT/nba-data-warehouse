from src.extract.nba_api_client import buscar_elenco, buscar_estatisticas_time
from src.transform.limpeza import remover_linhas_totais, corrigir_tipos_numericos
from src.models.estatistica_temporada import criar_estatistica_a_partir_da_linha
from src.load.database import criar_banco, inserir_estatisticas
from src.load.database import CAMINHO_BANCO
import sqlite3

# 1. Extração
df_elenco = buscar_elenco(team_id=1610612747)
df_bruto, falhas = buscar_estatisticas_time(team_id=1610612747)

# 2. Transformação
df_limpo = remover_linhas_totais(df_bruto)
df_limpo = corrigir_tipos_numericos(df_limpo)

# 3. Modelagem
lista_estatisticas = [criar_estatistica_a_partir_da_linha(linha) for _, linha in df_limpo.iterrows()]

# 4. Carga
criar_banco()
inserir_estatisticas(lista_estatisticas, df_elenco)

print(f"Concluído: {len(lista_estatisticas)} registros processados")

conexao = sqlite3.connect(CAMINHO_BANCO)
print(conexao.execute("SELECT COUNT(*) FROM dim_jogador").fetchone())
print(conexao.execute("SELECT COUNT(*) FROM dim_time").fetchone())
print(conexao.execute("SELECT COUNT(*) FROM fato_estatisticas_temporada").fetchone())
conexao.close()
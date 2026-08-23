from src.extract.nba_api_client import buscar_estatisticas_time
from src.transform.limpeza import remover_linhas_totais, corrigir_tipos_numericos
from src.models.estatistica_temporada import criar_estatistica_a_partir_da_linha

df_bruto, falhas = buscar_estatisticas_time(team_id=1610612747)
df_limpo = remover_linhas_totais(df_bruto)
df_limpo = corrigir_tipos_numericos(df_limpo)

lista_estatisticas = [criar_estatistica_a_partir_da_linha(linha) for _, linha in df_limpo.iterrows()]
print(lista_estatisticas[0])
print(len(lista_estatisticas))
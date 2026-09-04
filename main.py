from src.extract.nba_api_client import buscar_elenco, buscar_estatisticas_time
from src.transform.limpeza import remover_linhas_totais, corrigir_tipos_numericos
from src.models.estatistica_temporada import criar_estatistica_a_partir_da_linha
from src.load.database import criar_banco, inserir_estatisticas


def main():
    team_id = 1610612747  # Lakers

    df_elenco = buscar_elenco(team_id=team_id)
    df_bruto, falhas = buscar_estatisticas_time(team_id=team_id)

    df_limpo = remover_linhas_totais(df_bruto)
    df_limpo = corrigir_tipos_numericos(df_limpo)

    lista_estatisticas = [
        criar_estatistica_a_partir_da_linha(linha)
        for _, linha in df_limpo.iterrows()
    ]

    criar_banco()
    inserir_estatisticas(lista_estatisticas, df_elenco)

    print(f"Concluído: {len(lista_estatisticas)} registros processados")
    if falhas:
        print(f"Falhas: {falhas}")


if __name__ == "__main__":
    main()